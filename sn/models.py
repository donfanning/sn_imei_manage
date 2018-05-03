#-*- coding: UTF-8 -*- 
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Product(models.Model):
	#name = models.CharField(max_length=12,unique=True)
	name = models.CharField(max_length=20,validators=[
		RegexValidator(regex='^AC(\\d{5})-(\\d{4})$',message='Length has to be 12 and start with AC,like AC02345-1234')
		])

	class Meta:
		verbose_name = '产品型号'
		verbose_name_plural = '产品型号'

	def __str__(self):
		return self.name

	def get_product_start_sn(self):
		return self.name[3:7]+self.name[8:12]+'0000000'
	def get_last_record(self):
		return Record.objects.filter(product=self).order_by('-created_at').first()
	def get_record_count(self):
		return Record.objects.filter(product=self).count()

	def get_record_total_num(self):
		records = Record.objects.filter(product=self).all()
		total_num = 0
		for record in records:
			total_num += record.total
		return total_num

class Factory(models.Model):
	name = models.CharField(max_length=50,unique=True)

	class Meta:
		verbose_name = _("Factory")
		verbose_name_plural = _("Factory")
	
	def __str__(self):
		return self.name

class Record(models.Model):
	product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='records')
	current_first_sn = models.CharField(max_length=50)
	current_last_sn = models.CharField(max_length=50)
	total = models.PositiveIntegerField(verbose_name=_("Total"))
	factory = models.ForeignKey(Factory,on_delete=models.CASCADE,related_name='records',verbose_name = _("Factory"))
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='records')
	created_at = models.DateTimeField(auto_now_add=True)
	created_times = models.PositiveIntegerField(default=0)

	def __str__(self):
		return '{0}'.format(self.product)

	# def clean(self):
	# 	if self.total>10:
	# 		raise ValidationError('该号段申请数量已超最大限制9999999，请联系管理员')	
	class Meta:
		verbose_name = '申请记录'
		verbose_name_plural = '申请记录'	
