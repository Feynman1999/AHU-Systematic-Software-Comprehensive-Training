from queue import PriorityQueue as PQueue
import json,os
import numpy as np

from .RandomData import RandomData

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
    WaitQueue  = PQueue()                                   # 等待队列，数据结构为优先队列
    
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
    def WriteFile(self):
        TmpTime = 0     # 保存这组安全序列需要的时间
        TmpQueue = []   # 保存序列，用于恢复
        # 遍历优先队列，得到总时间
        while self.WaitQueue.empty() == False:
            Tmp = self.WaitQueue.get()
            TmpQueue.append(Tmp)
            if self.WaitQueue.qsize() == 0:
                TmpTime = Tmp.NeedTime

        # 优化剪枝条件
        self.TimeMinl = min(self.TimeMinl,TmpTime)
        for it in TmpQueue:
            self.WaitQueue.put(it)
        # 写入指定json文件
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
    
    # 用于外部调用，开始查找安全序列
    def Run(self):
        self.Answer=[None]*self.NumCustom
        self.Search(0,self.SystemInit,self.CustomInit,True,0)

        
    # DFS的过程，每次需要当前的状态
    def Search(self,TimeNow,System,AllocatedSource,CanAlloc,deep):
        if self.NumSafe >= 100:
            return
        if CanAlloc == False:                   # 无法分配，释放资源，时间跳到下一个节点
            if self.WaitQueue.qsize() == 0:     # 死锁，直接返回
                return 
            else:                               # 出队
                tmp = self.WaitQueue.get()
                TimeNow = TimeNow + tmp.NeedTime
                for i in range(len(self.MaxSource[tmp.Custom])):
                    System[i] = System[i] + self.MaxSource[tmp.Custom][i]

        if TimeNow > self.TimeMinl:            # 剪枝条件
            return
        if deep == self.NumCustom:              # 得到安全序列，输出到文件，回溯
            self.NumSafe = self.NumSafe + 1
            self.WriteFile()
            return

        CustomNeed = [None] * self.NumCustom
        for key in range(len(self.MaxSource)):  # 得到当前用户需要的资源数量
            CustomNeed[key] = [None]*self.NumResource
            for i in range(len(self.MaxSource[key])):
                CustomNeed[key][i] = self.MaxSource[key][i] - AllocatedSource[key][i]

        for key in range(len(self.MaxSource)):  # 判断是否能进行分配
            if key in self.Answer:
                continue
            flag = False                        # flag为False为能分配
            for i in range(len(CustomNeed[key])):
                if System[i] < CustomNeed[key][i]:
                    flag = True;break
            if flag == False:
                CanAlloc = True
                for i in range(len(CustomNeed[key])):       # 扣除该用户需要的资源
                    System[i] = System[i] - CustomNeed[key][i]
                    AllocatedSource[key][i] = self.MaxSource[key][i]
                # 标记安全序列
                self.Answer[deep] = key
                self.WaitQueue.put(Node(self.NeedTime[key] + TimeNow,key))
                self.Search(TimeNow,System,AllocatedSource,CanAlloc,deep+1)     
                self.Answer[deep] = None
                # 满足分配条件，进行分配
            else:
                CanAlloc = False
                    
        if CanAlloc == False: # 不满足分配条件，进入递归
            self.Search(TimeNow,System,AllocatedSource,CanAlloc,deep)

def allocation(NumCustom,NumSource):
    DataMaker = RandomData()
    Available, MaxSource, AllocatedSource, NeedTime=DataMaker.random_Data(NumCustom,NumSource,10000)
    test = AllocatCls(NumCustom,NumSource)
    test.LoadData(Available, MaxSource, AllocatedSource, NeedTime)
    test.Run()