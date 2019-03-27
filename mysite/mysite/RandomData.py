import numpy as np
import operator

class customer(object):
        def __init__(self, Max, Allocated, Need):
            self.Max = Max
            self.Allocated = Allocated
            self.Need = Need
        def __repr__(self):
            return repr((self.Max, self.Allocated, self.Need))

class RandomData(object):   
    def __init__(self):
        pass
    
    def random_Data(self,n, m, SourceMaximum):#n是客户的数量，m是资源的种类，SourceMaximum是资源的最高阈值
        if SourceMaximum < 100:#资源最大阈值太小报错
            print ("The maximum of source is too small!!!")
        else:
            Available = np.random.uniform(SourceMaximum-10, SourceMaximum, m).round().tolist()#生成剩余系统资源，均匀分布
            OriginalMaxSource = np.random.normal((SourceMaximum-10) * 13/30, (SourceMaximum-10) * 7/90, [n,m]).round().tolist()#生成客户对每种资源最大需求量；前两个参数分别为均值、标准差，常数因子的目的是为了让其数据分布满足特定均值、特定范围的正态分布
            OriginalAllocatedSource = np.random.normal((SourceMaximum-10) / 10, (SourceMaximum-10) / 30, [n,m]).round().tolist()#生成客户每种资源的已经拥有量，方法与上述类似
            OriginalNeedTime = np.random.uniform(1, n, n).round().tolist()#生成客户对资源的占用时间，均匀分布
            CustomerList = [customer(OriginalMaxSource[i], OriginalAllocatedSource[i], OriginalNeedTime[i]) for i in range(n)]  #用客户类将生成的数据封装
            CmpFun = operator.attrgetter('Need')  #下面排序用到的比较函数
            CustomerList.sort(key = CmpFun)  #对客户按时间进行排序
            MaxSource = [CustomerList[i].Max for i in range(n)]  #将排序后的列表中的数据分离
            AllocatedSource = [CustomerList[i].Allocated for i in range(n)]
            NeedTime = [CustomerList[i].Need for i in range(n)]
            return (Available, MaxSource, AllocatedSource, NeedTime)  #返回随机数据的四元组