#-*- coding: UTF-8 -*- 
from django.contrib import admin
from .models import Product,Factory,Record
from django.db.models import F
from django.http import HttpResponse
import csv
# Register your models here.


def export_records(modeladmin,reuest,queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment;filename="imei.csv'
	writer = csv.writer(response)
	writer.writerow(['产品型号','起始SN','结束SN'])
	records = queryset.values_list('product__name','current_first_sn','current_last_sn')
	for record in records:
		writer.writerow(record)
	return response

export_records.short_description = '导出到CSV文件'

class RecordAdmin(admin.ModelAdmin):
	fields = ['factory']
	#fields = ['current_first_sn','current_last_sn','factory']
	list_display = ('product','current_first_sn','current_last_sn','created_at','total')
	list_filter = ['created_at']
	search_fields = ['product__name'] #product is a foreign key,it must use __icontains 
	actions = [export_records,]

admin.site.register(Product)
admin.site.register(Factory)
admin.site.register(Record,RecordAdmin)
