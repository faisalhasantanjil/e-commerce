from django.contrib import admin
from .models import Category, Tree, UserProfile, Orders, OrderItems

# Register your models here. 

admin.site.register(Category)
admin.site.register(Tree)
admin.site.register(UserProfile)
admin.site.register(Orders)
admin.site.register(OrderItems)