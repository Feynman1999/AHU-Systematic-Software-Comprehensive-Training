import random
import os
import json
import math

from django.conf import settings

data_dir = os.path.join(settings.BASE_DIR,'static\\experiment\\data\\')

# allocation_l allocation_r need_l need_r time_l time_r available_l available_r
para = [1,100,1,100,1,240]

def init_allocation(n,m):
    return [[random.randint(para[0], para[1]) for j in range(1, m+1)] for i in range(1, n+1)]


def init_need(n,m):
    return [[random.randint(para[2], para[3]) for j in range(1, m+1)] for i in range(1, n+1)]


def init_time(n):
    return [random.randint(para[4], para[5]) for i in range(1, n+1)] 


def init_available(n, m):
    return [random.randint(para[6], para[7]) for j in range(1, m+1)]  


def init_basic(Id, n ,m):
    para.append(math.ceil(n/4)*para[2])
    para.append(math.ceil(n/4)*para[3])
    file_name = os.path.join(data_dir, str(Id) + "_basic.json") 
    Dict = {}
    Dict["nnn"] = n
    Dict["mmm"] = m
    Dict['n_id'] = list(range(1, n+1))
    Dict['m_id'] = list(range(1, m+1))
    Dict["allocation"] = init_allocation(n, m)
    Dict["need"] = init_need(n, m)
    Dict["time"] = init_time(n)
    Dict["available"] = init_available(n, m)
    Dict["para"] = para
    with open(file_name, 'w') as f:
        json.dump(Dict, f)

#随机生成安全序列用于前端的测试
def generate_safe_random(experiment_id):
    #根据experimen_id读取相应json中的数据
    file_name = os.path.join(data_dir, str(experiment_id))
    with open(file_name+"_basic.json",'r') as load_f:
        Dict = json.load(load_f)
    nnn = Dict['nnn']#该实验最多的人数
    seq = list(range(1,nnn+1))
    random.shuffle(seq)
    useTime = random.randint(1,10)
    return seq,useTime