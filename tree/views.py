from urllib import response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from .forms import *
from .decorators import *

# Create your views here.

def home(request):
    return render(request, 'tree/home.html')

def signin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()

    return render(request, 'tree/signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        user_form = UserSignupForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = UserSignupForm()
        profile_form = UserProfileForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'tree/signup.html', context)

@login_required(login_url='signin')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'tree/change_password.html', {'form': form})


def user_profile(request):
    pass

def create_product(request):
    pass


def update_product(request,pk):
    pass

def delete_product(request,pk):
    pass


def products(request):
    pass

def product_details(request,pk):
    pass

def add_to_cart(request):
    pass

def place_order(request):
    pass

def orders(request):
    pass

def order_details(request):
    pass


 
@login_required(login_url='login')  # Restrict access if needed
def category_list(request):
  categories = Category.objects.all()
  return render(request, 'tree/category_list.html', {'categories': categories})

@login_required
def category_details(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'tree/category_details.html', {'category': category})

@login_required(login_url='login')  # Restrict access if needed
def category_form(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('category_list')
  else:
    form = CategoryForm()
  return render(request, 'tree/category_form.html', {'form': form})

@login_required(login_url='login')  # Restrict access if needed
def category_update(request, pk):
  category = Category.objects.get(pk=pk)
  if request.method == 'POST':
    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
      form.save()
      return redirect('category_list')
  else:
    form = CategoryForm(instance=category)
  return render(request, 'tree/category_form.html', {'form': form})

@login_required(login_url='signin')  # Restrict access if needed
def category_delete(request, pk):
  category = Category.objects.get(pk=pk)
  if request.method == 'POST':
    category.delete()
    return redirect('category_list')

#@login_required(login_url='signin')  # Restrict access if needed
def tree_list(request):
  trees = Tree.objects.all().order_by('-id')
  return render(request, 'tree/tree_list.html', {'trees': trees})

@login_required
def tree_details(request, pk):
    tree = get_object_or_404(Tree, pk=pk)
    order_exist = OrderItem.objects.filter(user=request.user,tree= tree,ordered=False).first()
    #print(order_exist)
    if order_exist:
        form= OrderItemForm(instance=order_exist)
        if request.method == 'POST':
                form = OrderItemForm(request.POST, instance=order_exist)
                if form.is_valid():
                    order_item = form.save(commit=False)
                    order_item.user = request.user
                    order_item.tree= tree
                    order_item.save()
                    return HttpResponseRedirect(request.path_info)
        context= {
        'tree': tree,
        'form': form
        }
    else:
        form= OrderItemForm()
        if request.method == 'POST':
            form = OrderItemForm(request.POST)
            if form.is_valid():
                order_item = form.save()
                order_item.user = request.user
                order_item.tree= tree
                order_item.save()
                return HttpResponseRedirect(request.path_info)
        
        context= {
        'tree': tree,
        'form': form
        }
    #print(dir(request.user))
    print(request.user.is_staff)
    return render(request, 'tree/tree_details.html', context)

@login_required
def tree_details_admin(request, pk):
    tree = get_object_or_404(Tree, pk=pk)
    print(tree.image.url)
    return render(request, 'tree/tree_details_admin.html', {'tree': tree})

@login_required(login_url='signin')
@staff_access_only()  # Restrict access if needed
def tree_form(request):
  if request.method == 'POST':
    form = TreeForm(request.POST, request.FILES)  # Include request.FILES for image upload
    if form.is_valid():
      form.save()
      return redirect('tree_list')
  else:
    form = TreeForm()
  return render(request, 'tree/tree_form.html', {'form': form})

@login_required(login_url='signin')  # Restrict access if needed
def tree_update(request, pk):
  tree = Tree.objects.get(pk=pk)
  if request.method == 'POST':
    form = TreeForm(request.POST, request.FILES, instance=tree)  # Include request.FILES for image upload
    if form.is_valid():
      form.save()
      return redirect('tree_list')
  else:
    form = TreeForm(instance=tree)
  return render(request, 'tree/tree_form.html', {'form': form})

@login_required(login_url='signin')  # Restrict access if needed
def tree_delete(request, pk):
  tree = Tree.objects.get(pk=pk)
  tree.delete()
  return redirect('tree_list')


@login_required
def order(request):
    orders = OrderItem.objects.filter(user=request.user, ordered= False)
    previous_orders = OrderItem.objects.filter(user=request.user, ordered= True)
    form= OrderForm()
    context={
       'orders':orders,
       'previous_orders': previous_orders,
       'form': form,
    }
    
    return render(request, 'tree/order_item_form.html', context)

@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        orders = OrderItem.objects.filter(user=request.user, ordered= False)
        if form.is_valid():
            order_placed = form.save(commit=False)
            order_placed.user = request.user
            order_placed.save()
            #order_placed.items.add(*[item for item in orders if not item.ordered])
            for item in orders:
                if not item.ordered:
                    order_placed.items.add(item)
                    item.ordered = True
                    item.save()

            order_placed.save()
            #form.save_m2m
        order_items= order_placed.items.all()
    
    context={
       'order_placed':order_placed,
       'order_items':order_items,
    }
    
    return render(request, 'tree/order_confirm.html', context)




'''
@login_required
def order_item_update(request, order_pk, pk):
    order = get_object_or_404(Order, pk=order_pk, user=request.user)
    order_item = get_object_or_404(OrderItem, pk=pk, order=order)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderItemForm(instance=order_item)
    return render(request, 'tree/order_item_form.html', {'form': form})
'''

@login_required
def order_item_delete(request, pk):
    order_item = get_object_or_404(OrderItem, id=pk)
    if order_item:
        order_item.delete()
        return HttpResponseRedirect(reverse('tree_details', kwargs={'pk': order_item.tree.id}))
    orders = OrderItem.objects.filter(user=request.user, ordered= False)
    previous_orders = OrderItem.objects.filter(user=request.user, ordered= True)
    context={
       'orders':orders,
       'previous_orders': previous_orders
    }
    
    return render(request, 'tree/order_item_form.html', context)

###########################################################################################################################

'''
#ADMIN-------------
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'tree/order_list.html', {'orders': orders})
'''
#ADMIN-------------
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'tree/order_list.html', {'orders': orders})

#ADMIN-------------
@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'tree/order_detail.html', {'order': order})
#ADMIN-------------
@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'tree/order_form.html', {'form': form})
#ADMIN-------------
@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'tree/order_form.html', {'form': form})
#ADMIN-------------
@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'tree/order_confirm_delete.html', {'order': order})