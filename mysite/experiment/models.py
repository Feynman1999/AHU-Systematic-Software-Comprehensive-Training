from django.db import models


class ExperimentType(models.Model):
    type_name = models.CharField(max_length=60)
    def __str__(self):
        return self.type_name


class Experiment(models.Model):
    title = models.CharField(max_length = 120)
    experiment_type = models.ForeignKey(ExperimentType, on_delete=models.CASCADE, default = 1)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Experiment: {}".format(self.title)

    class Meta:
        ordering = ['-created_time']  # 按照时间倒叙排列

