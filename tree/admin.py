from django.contrib import admin
from .models import Category, Tree, UserProfile, Order, OrderItem

# Register your models here. 

admin.site.register(Category)
admin.site.register(Tree)
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(OrderItem)