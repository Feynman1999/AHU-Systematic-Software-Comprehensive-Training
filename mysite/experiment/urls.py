from .views import * 
from django.urls import path

# start with /experiment/
urlpatterns = [
    path('', experiment_list, name='experiment_list'),
    path('update_n', update_n, name='update_n'),
    path('<int:experiment_id>', experiment_detail, name='experiment_detail'),
    path('type/<int:type_id>', experiment_list_with_type , name='experiment_list_with_type'),
]   