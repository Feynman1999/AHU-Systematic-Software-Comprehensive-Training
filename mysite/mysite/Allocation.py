from queue import PriorityQueue as PQueue
import json,os,copy
import numpy as np
class Node(object):
    def __init__(self,NeedTime,Custom):
        self.NeedTime = NeedTime
        self.Custom = Custom
    # 定义小于号，用于在优先队列中的存储
    def __lt__(self,other):
        # redefined operator < 
        return self.NeedTime < other.NeedTime
# 封装好的类，用户输入数据之后直接调用run方法得到结果
class AllocatCls(object):   
    TimeMinl = 1<<30                                        # 剪枝条件：最少花费时间
    NumCustom = 0                                           # 客户数量
    NumResource = 0                                         # 资源数量
    NumSafe = 0                                             # 安全序列的个数
    OutFileName = "SecurityList.json"                       # 写数据的文件名
    
    Answer = []                                             # 记录的安全序列    
    NeedTime = []                                           # 用户完成任务所需时间
    MaxSource = []                                          # 用户一共所需要的资源量
    CustomInit = []                                         # 用户初始资源量
    SystemInit = []                                         # 系统初始有的资源量
    # WaitQueue  = PQueue()                                   # 等待队列，数据结构为优先队列
    
    # 类的初始化，需要输入用户数量和资源数量
    def __init__(self,NumCustom,NumResource):              
        self.NumCustom = NumCustom
        self.NumResource = NumResource
    
    # 等待传入参数
    def LoadData(self,Available,MaxSource,AllocatedSource,NeedTime):                    
        self.SystemInit = Available
        self.MaxSource = MaxSource
        self.CustomInit = AllocatedSource
        self.NeedTime = NeedTime
        
    # 把得到的安全序列输入到指定文件
    def WriteFile(self,WaitQueue):
        # print('************safe***************')
        # print(self.Answer,'\n\n\n\n')
        TmpTime = 0     # 保存这组安全序列需要的时间
        TmpQueue = []   # 保存序列，用于恢复
        # 遍历优先队列，得到总时间
        while WaitQueue.empty() == False:
            Tmp = WaitQueue.get()
            TmpQueue.append(Tmp)
            if WaitQueue.qsize() == 0:
                TmpTime = Tmp.NeedTime

        # 优化剪枝条件
        self.TimeMinl = min(self.TimeMinl,TmpTime)
        for it in TmpQueue:
            WaitQueue.put(it)
        # 写入指定json文件
        if os.path.exists(self.OutFileName):
            size = os.path.getsize('./'+self.OutFileName)
            with open(self.OutFileName,'r') as file_object:
                now = file_object.read()
            with open(self.OutFileName,'w') as file_object:
                if  size ==0:
                    tmp=dict()
                else:
                    tmp = json.loads(now)
                tmp[self.NumSafe]=(self.Answer,TmpTime)
                json.dump(tmp,file_object,indent=4)
        else:
            with open(self.OutFileName,'w') as file_object:
                tmp=dict()
                tmp[self.NumSafe]=(self.Answer,TmpTime)
                json.dump(tmp,file_object,indent=4)
        
    
    # 用于外部调用，开始查找安全序列
    def Run(self):
        self.Answer=[None]*self.NumCustom
        self.Search(0,self.SystemInit,self.CustomInit,True,0,PQueue())

        
    # DFS的过程，每次需要当前的状态
    def Search(self,TimeNow,System,AllocatedSource,CanAlloc,deep,WaitQueue):
        # print('Time=',TimeNow)
        # print('System=',System)
        # print('AllocatedSource=',AllocatedSource)
        # print('CanAlloc=',CanAlloc)
        # print('Deep=',deep)
        # print("QueueSize=",WaitQueue.qsize())
        # que=[]
        # while WaitQueue.empty() == False:
        #     tmp=WaitQueue.get()
        #     print('Time=',tmp.NeedTime)
        #     print('Custom=',tmp.Custom,'\n')
        #     que.append(tmp)
        # for i in que:
        #     WaitQueue.put(i)
        # print('Answer=',self.Answer,'\n\n')
        # if self.NumSafe >= 100:
        #     return
        if CanAlloc == False:                   # 无法分配，释放资源，时间跳到下一个节点
            if WaitQueue.qsize() == 0:     # 死锁，直接返回
                return 
            else:                               # 出队
                tmp = WaitQueue.get()
                TimeNow = TimeNow + tmp.NeedTime
                for i in range(self.NumResource):
                    System[i] = System[i] + self.MaxSource[tmp.Custom][i]

        if TimeNow > self.TimeMinl:            # 剪枝条件
            return
        if deep == self.NumCustom:              # 得到安全序列，输出到文件，回溯
            self.NumSafe = self.NumSafe + 1
            self.WriteFile(WaitQueue)
            return

        CustomNeed = [None] * self.NumCustom
        for key in range(self.NumCustom):  # 得到当前用户需要的资源数量
            CustomNeed[key] = [None]*self.NumResource
            for i in range(self.NumResource):
                CustomNeed[key][i] = self.MaxSource[key][i] - AllocatedSource[key][i]

        for key in range(self.NumCustom):  # 遍历每个用户判断是否能进行分配
            if key in self.Answer:# 判定重复
                continue
            flag = False                        # flag为False为能分配
            for i in range(self.NumResource):
                if System[i] < CustomNeed[key][i]:
                    flag = True;break
            if flag == False:
                CanAlloc = True
                # 深拷贝一堆参数
                TmpAllcatedSource = copy.deepcopy(AllocatedSource) 
                TmpSystem = copy.deepcopy(System)
                TmpQueue = PQueue()
                TmpVector = []
                while WaitQueue.empty() == False:
                    Tmp = copy.deepcopy(WaitQueue.get())
                    Tmp.append(Tmp)
                    TmpQueue.put(Tmp) 
                for it in TmpVector:
                    WaitQueue.put(it)
                # print('TmpSystem=',TmpSystem)
                # print('TmpAllcatedSource=',TmpAllcatedSource)
                # print('AllocatedSource=',AllocatedSource)
                # print('Need=',CustomNeed)

                for i in range(self.NumResource):       # 扣除该用户需要的资源
                    TmpSystem[i] = System[i] - CustomNeed[key][i]
                    TmpAllcatedSource[key][i] = self.MaxSource[key][i]
                # 标记安全序列
                self.Answer[deep] = key
                TmpQueue.put(Node(self.NeedTime[key] + TimeNow,key))
                # print('Key=',key)
                # print('AfterTmpSystem=',TmpSystem)
                # print('AfterTmpAllcatedSource=',TmpAllcatedSource)
                self.Search(TimeNow,TmpSystem,TmpAllcatedSource,CanAlloc,deep+1,TmpQueue)     
                # 满足分配条件，进行分配
                self.Answer[deep] = None

            else:
                CanAlloc = False
                    
        if CanAlloc == False: # 不满足分配条件，进入递归
            self.Search(TimeNow,System,AllocatedSource,CanAlloc,deep,WaitQueue)


if __name__ == "__main__":
    with open('data.json','r') as file_object:
            now = file_object.read()
    data = json.loads(now)
    Available = data['Available']
    MaxSource = data['MaxSource']
    AllocatedSource = data['AllocatedSource']
    NeedTime = data['NeedTime']
    test = AllocatCls(3,3)
    test.LoadData(Available, MaxSource, AllocatedSource, NeedTime)
    test.Run()