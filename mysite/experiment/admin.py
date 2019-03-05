from django.contrib import admin
from .models import Experiment, ExperimentType


@admin.register(ExperimentType)
class ExperimentType_Admin(admin.ModelAdmin):
    list_display = ('id', 'type_name')



@admin.register(Experiment)
class Experiment_Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'experiment_type', 'created_time', 'last_updated_time')
    ordering = ('-created_time', ) # admin中类对象的显示顺序

