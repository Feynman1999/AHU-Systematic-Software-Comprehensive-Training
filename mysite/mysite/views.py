from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse

from experiment.models import ExperimentType

def index(request):
    Dict = {}
    Dict['types'] = ExperimentType.objects.all()
    return render(request, 'index.html', Dict)


def about(request):
    return render(request, 'about.html')


def result_list(request):
    return render(request, 'result_list.html')