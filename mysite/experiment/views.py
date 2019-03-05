import os, json, time
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist


from .models import Experiment, ExperimentType
from .random_init import *


def SuccessResponse(data):
    data['status'] = 'SUCCESS'
    cache.set('get_nnn_chart', time.time())
    print(time.time())
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


# 添加一条顾客信息
def update_n(request):
    print(time.time())
    time_gap = cache.get('get_nnn_chart')
    if (not time_gap is None) and time.time()-time_gap < 0.4:
        return ErrorResponse(403, '操作过于频繁! limit: 400ms')
    data = {}
    lastn = int(request.GET.get("lastn", 0))
    nnn= int(request.GET.get("nnn", 0))
    if lastn>=nnn:
        return ErrorResponse(402, '已经显示所有顾客数据')
    experiment_id = request.GET.get("experiment_id", 1)
    file_name = os.path.join(data_dir, str(experiment_id))

    Dict = cache.get('experiment_'+str(experiment_id))
    if Dict is None: # 只要经过正常途径创建 这不可能！
        raise ObjectDoesNotExist 

    # 只需要n_id need allocation
    data['allocation'] = Dict['allocation'][lastn]
    data['need'] = Dict['need'][lastn]
    data['n_id'] = Dict['n_id']

    return SuccessResponse(data)
    


def make_pagination(request, experiments_all):
    paginator = Paginator(experiments_all, settings.NUM_IN_ONE_PAGE)
    page_of_experiments = paginator.get_page(request.GET.get("page", 1))
    page_id_now = page_of_experiments.number
    page_range = [ i for i in range(page_id_now-settings.PAGE_GAP,page_id_now+settings.PAGE_GAP+1)]
    if settings.PAGE_GAP*2+1 > page_of_experiments.paginator.num_pages: # 如果页很少 就显示这些页
        page_range = [i for i in range(1, page_of_experiments.paginator.num_pages+1)]
    elif page_range[0] < 1: #否则若前面超界 
        page_range = [i for i in range(1, 2*settings.PAGE_GAP+1+1)]
    elif page_range[-1] > page_of_experiments.paginator.num_pages: #否则若后面超界 
        page_range = [i for i in range(page_of_experiments.paginator.num_pages-2*settings.PAGE_GAP, page_of_experiments.paginator.num_pages+1)]
    return page_range, page_of_experiments


def init_dict(request, experiments_all):
    Dict = {}
    # 统计每个类别有多少实验
    experiment_types = ExperimentType.objects.all()
    experiment_types_list=[]
    for experiment_type in experiment_types:
        experiment_type.experiment_count = Experiment.objects.filter(experiment_type=experiment_type).count() # 直接加入新的属性
        experiment_types_list.append(experiment_type)
    Dict['experiment_types'] = experiment_types_list
    Dict['page_range'], Dict['page_of_experiments'] = make_pagination(request, experiments_all) # 要显示的页码
    return Dict


def experiment_list(request):
    experiments_all = Experiment.objects.all()
    Dict = init_dict(request, experiments_all)
    return render(request, "experiment/experiment_list.html", Dict)



def experiment_list_with_type(request, type_id):
    experiment_type = get_object_or_404(ExperimentType, pk=type_id)
    experiments_all = Experiment.objects.filter(experiment_type=experiment_type)
    Dict = init_dict(request, experiments_all)
    Dict['experiment_type'] = experiment_type
    return render(request, "experiment/experiment_list_with_type.html", Dict)


# 读取相关数据
def deal_Dict(experiment_id):
    Dict={}
    Dict['experiment_id'] = experiment_id
    file_name = os.path.join(data_dir, str(experiment_id))
    if os.path.exists(file_name+"_basic.json"):
        if os.path.exists(file_name+"_sequence.txt"):
            Dict['status_mark'] = 2
        else:
            Dict['status_mark'] = 1
            Dict2 = cache.get('experiment_'+str(experiment_id))
            if Dict2 is None:
                with open(file_name+"_basic.json",'r') as load_f:
                    Dict2 = json.load(load_f)
                    cache.set('experiment_'+str(experiment_id), Dict2)
            for k,v in Dict2.items():
                Dict[k]=v
    else:
        Dict['status_mark'] = 0
    return Dict


def experiment_detail(request, experiment_id):
    if request.method == 'POST':
        obj_title = request.POST.get('title')
        obj_nnn =  int(request.POST.get('nnn'))
        obj_mmm =  int(request.POST.get('mmm'))

        if obj_mmm<=1 or obj_nnn<=1 or obj_mmm>settings.NUM_UP or obj_nnn>settings.NUM_UP:
            return render(request, 'error.html', {'message': '请保证数量在2~{}范围之间'.format(settings.NUM_UP), 'redirect_to': reverse('index')})
        
        obj_type = get_object_or_404(ExperimentType, type_name=request.POST.get('type'))
        new_obj = Experiment.objects.create(title=obj_title,
                                            experiment_type=obj_type)
        # 初始化数据 生成文件
        init_basic(new_obj.pk, obj_nnn, obj_mmm)
        referer = reverse('experiment_detail', kwargs={'experiment_id':new_obj.pk})
        return redirect(referer)
    elif request.method == 'GET':
        experiment = get_object_or_404(Experiment, pk = experiment_id)
        Dict = deal_Dict(experiment_id)
        Dict['experiment'] = experiment
        Dict['previous_experiment'] = Experiment.objects.filter(created_time__gt=experiment.created_time).last()
        Dict['next_experiment'] = Experiment.objects.filter(created_time__lt=experiment.created_time).first()
        response = render(request, "experiment/experiment_detail.html", Dict)
        return response
    else:
        pass
        return redirect(reverse('index'))