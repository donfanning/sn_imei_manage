#-*- coding: UTF-8 -*- 
from django import forms
from .models import Product,Factory,Record
from django.urls import reverse
from django.core.exceptions import ValidationError



class NewRecordForm(forms.ModelForm):
	#place_id = forms.CharField(widget=forms.HiddenInput(),required=True)
	class Meta:			
		model = Record
		fields = ['factory','total']


	# def clean(self):
	# 	cleaned_data=super().clean()
	# 	if self.cleaned_data["total"]>10:
	# 		raise ValidationError('该号段申请数量已超最大限制9999999，请联系管理员')