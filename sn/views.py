#-*- coding:utf-8
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,permission_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView
from .models import Product,Factory,Record
from .forms import NewRecordForm
from django.core.exceptions import ValidationError

# Create your views here.

# 使用通用视图函数
# class PorductListView(ListView):
# 	model = Product
# 	context_object_name = 'products'
# 	template_name = 'home.html'

def home(request):
	products = Product.objects.all()
	return render(request,'home.html',{'products':products})


def product_records(request,pk):
	product = get_object_or_404(Product,pk=pk)
	queryset = product.records.order_by('-created_at')
	page  = request.GET.get('page',1)
	paginator = Paginator(queryset,10)
	try:
		records = paginator.page(page)
	except PageNotAnInteger:
		records = paginator.page(1)
	except EmptyPage:
		records = paginator.page(paginator.num_pages)
	return render(request,'product_records.html',{'product':product,'records':records})

@login_required
@permission_required('request.user.is_staff')
def new_record(request,pk):
	product = get_object_or_404(Product,pk=pk)
	if request.method == 'POST':
		form = NewRecordForm(request.POST)
		if form.is_valid():
			record = form.save(commit=False)
			if record.total+product.get_record_total_num()>9999999:
				raise ValidationError('该号段申请数量已超最大限制9999999，请联系管理员')
				return render(request,'new_record.html',{'product':product,'form':form})
				#pass
			else:
				if product.get_record_count()==0:
					endsn = int(product.name[3:7]+product.name[8:12]+'0000000')
				else:
					endsn = int(product.get_last_record().current_last_sn)
				record.product = product
				record.current_first_sn = '{0}'.format(endsn+1)
				record.current_last_sn = '{0}'.format((int(record.current_first_sn)+record.total-1))
				record.created_by = request.user
				record.save()
				return redirect('product_records',pk=product.pk)
	else:
		form = NewRecordForm()

	return render(request,'new_record.html',{'product':product,'form':form})