from django import forms
from django.db.models import ObjectDoesNotExist
from .models import Experiment, ExperimentType


class AddExperimentForm(forms.Form):
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(min_length=5, 
                           widget=forms.Textarea(attrs={'class':'form-control', 'id':'forclear',
                                'placeholder':"至少写入5个字符哦   支持markdown(刷新可渲染tex)~   \n\n点击下面回复可以对评论进行回复 \n\n刷新本页面时默认对文章进行评论",
                                "rows":"6"}), 
                           error_messages={'required': '评论内容不能为空哦'})

