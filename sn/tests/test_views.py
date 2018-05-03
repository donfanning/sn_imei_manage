from django.test import TestCase
from django.urls import reverse,resolve
from ..views import home,product_records,new_record
from ..models import Product,Record


class HomeTests(TestCase):
	def setUp(self):
		self.product = Product.objects.create(name='AC01')
		url = reverse('home')
		self.response = self.client.get(url)
	def test_home_view_status_code(self):
		self.assertEqual(self.response.status_code,200)

	def test_home_url_resolves_home_view(self):
		view = resolve('/')
		self.assertEqual(view.func,home)

	def test_home_view_contains_link_to_product_records_page(self):
		product_records_url = reverse('product_records',kwargs={'pk':self.product.pk})
		self.assertContains(self.response,'href="{0}"'.format(product_records_url))


class ProudctRecordsTests(TestCase):
	def setUp(self):
		self.product=Product.objects.create(name='AC01')
		product_records_url = reverse('product_records',kwargs={'pk':1})
		self.response = self.client.get(product_records_url)

	def test_product_records_view_success_status_code(self):
		self.assertEqual(self.response.status_code,200)

	def test_product_records_view_not_found_status_code(self):
		url = reverse('product_records',kwargs={'pk':2})
		response = self.client.get(url)
		self.assertEqual(response.status_code,404)

	def test_product_records_url_resolves_product_record_view(self):
		view = resolve('/products/1/')
		self.assertEqual(view.func,product_records)

	def test_prduct_records_view_contains_link_back_to_home_page(self):
		home_url = reverse('home')
		self.assertContains(self.response,'href="{0}"'.format(home_url))

	def test_prduct_records_view_contains_link_to_new_recod_page(self):
		new_record_url = reverse('new_record',kwargs={'pk':1})
		self.assertContains(self.response,'href="{0}"'.format(new_record_url))

