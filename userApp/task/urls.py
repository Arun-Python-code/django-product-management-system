"""
URL configuration for userApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('login/', views.Login_page, name='Login_page' ),
    path('sign/',  views.Sign_up, name='Sign_page'),
    path('home/', views.Home, name='Home_page'),
    path('addproduct/', views.Addproduct, name='Addproduct'),
    path('createuser/', views.created_user, name="createuser"),
    path('createproduct/', views.create_product, name="Createproduct"),
    path("loginuser/", views.login_user, name="Loginuser"),
    path("productlist/", views.product_list, name="Productslist"),
    path("updateproduct/<int:product_id>/", views.update_product, name="updateproduct"),
    path("deleteproduct/<int:product_id>/", views.delete_product, name="deleteproduct"),
    path("getproduct/<int:product_id>/", views.get_product, name="getproduct"),

]
