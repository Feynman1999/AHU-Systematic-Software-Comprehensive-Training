import numpy as np
import operator

class customer(object):  #客户类
        def __init__(self, Max, Allocated, Need):#分别对应最大需求量，已分配量，当前需求量
            self.Max = Max
            self.Allocated = Allocated
            self.Need = Need
        def __repr__(self):
            return repr((self.Max, self.Allocated, self.Need))

class RandomData(object):   
    def __init__(self):
        pass
    
    def random_Data(self, NumberCustomer, NumberSource, SourceMaximum):#NumberCustomer是客户的数量，NumberSource是资源的种类，SourceMaximum是资源的最高阈值
        if SourceMaximum < 100:#资源最大阈值太小报错
            print ("The maximum of source is too small!!!")
        else:
            Available = np.random.uniform(SourceMaximum * 4/5, SourceMaximum, NumberSource).round().tolist()#生成剩余系统资源，均匀分布
            OriginalMaxSource = np.random.normal((SourceMaximum* 4/5) * 0.5, (SourceMaximum* 4/5) * 1/10, [NumberCustomer,NumberSource]).round().tolist()#生成客户对每种资源最大需求量；前两个参数分别为均值、标准差，常数因子的目的是为了让其数据分布满足特定均值、特定范围的正态分布
            OriginalAllocatedSource = np.random.normal((SourceMaximum* 4/5) / 10, (SourceMaximum* 4/5) / 30, [NumberCustomer,NumberSource]).round().tolist()#生成客户每种资源的已经拥有量，方法与上述类似
            OriginalNeedTime = np.random.uniform(1, NumberCustomer, NumberCustomer).round().tolist()#生成客户对资源的占用时间，均匀分布
            CustomerList = [customer(OriginalMaxSource[i], OriginalAllocatedSource[i], OriginalNeedTime[i]) for i in range(NumberCustomer)]  #用客户类将生成的数据封装
            CmpFun = operator.attrgetter('Need')  #下面排序用到的比较函数
            CustomerList.sort(key = CmpFun)  #对客户按时间进行排序
            MaxSource = [CustomerList[i].Max for i in range(NumberCustomer)]  #将排序后的列表中的数据分离
            AllocatedSource = [CustomerList[i].Allocated for i in range(NumberCustomer)]
            NeedTime = [CustomerList[i].Need for i in range(NumberCustomer)]
            return (Available, MaxSource, AllocatedSource, NeedTime)  #返回随机数据的四元组