"""sn_imei_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from sn import views
from accounts import views as accounts_views

urlpatterns = [
	path('',views.home,name='home'),

    path('signup/',accounts_views.signup,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    
	path('products/<int:pk>/',views.product_records,name='product_records'),
	path('products/<int:pk>/new/',views.new_record,name='new_record'),

    path('settings/account/',accounts_views.UserUpdateView.as_view(),name='my_account'),
    path('settings/password/',auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    path('settings/password/done/',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    path('admin/', admin.site.urls),
]
