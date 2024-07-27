"""
URL configuration for plant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('change_password/', views.change_password, name='change_password'),

    path('category/', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_details, name='category_details'),
    path('category/new/', views.category_form, name='category_form'),
    path('category/<int:pk>/edit/', views.category_delete, name='category_delete'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('trees/', views.tree_list, name='tree_list'),
    path('trees/<int:pk>/', views.tree_details, name='tree_details'),
    path('trees/new/', views.tree_form, name='tree_form'),
    path('trees/<int:pk>/edit/', views.tree_update, name='tree_update'),
    path('trees/<int:pk>/delete/', views.tree_delete, name='tree_delete'),

    path('order/', views.order, name='order'),
    path('place_order/', views.place_order, name='place_order'),
    path('orders/<int:pk>', views.order_item_delete, name='order_item_delete'),


    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/new/', views.order_create, name='order_create'),
    path('orders/<int:pk>/edit/', views.order_update, name='order_update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('orders/<int:order_pk>/items/<int:pk>/delete/', views.order_item_delete, name='order_item_delete'),
]
