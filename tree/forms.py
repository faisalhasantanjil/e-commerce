from django import forms
from django.contrib.auth.models import User
from .models import *

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone']

class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ['name', 'description']

class TreeForm(forms.ModelForm):
  class Meta:
    model = Tree
    fields = ['name', 'category', 'description', 'size', 'price', 'quantity', 'image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address']
        '''
        def save(self, commit=True):
            instance = super().save()
            # Here, you can add logic to handle order placement confirmation,
            # such as setting the status or processing payment.
            for item in instance.items:
                item.ordered = True
                item.save()
            return instance
'''
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'is_paid']