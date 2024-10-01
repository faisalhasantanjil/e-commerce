from urllib import response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from .forms import *
from .decorators import *
from django.views import View
from django.conf import settings
from django.core.mail import send_mail

import stripe


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
  search_name = request.GET.get('name', '')
  if search_name:
     trees = trees.filter(name__icontains=search_name)
  staff = False
  if request.user.is_authenticated:
     staff = request.user.is_staff
  context = {
     'trees': trees,
     'staff': staff

  }
  return render(request, 'tree/tree_list.html',context)


def tree_details(request, pk):
    tree = get_object_or_404(Tree, pk=pk)

    if not request.user.is_authenticated:
       context= {
        'tree': tree,
        }
       
    else :
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
                    order_item = form.save(commit=False)
                    order_item.user = request.user
                    order_item.tree= tree
                    order_item.save()
                    return HttpResponseRedirect(request.path_info)
        context= {
        'tree': tree,
        'form': form
        }
    
    return render(request, 'tree/tree_details.html', context)

@login_required
def tree_details_admin(request, pk):
    tree = get_object_or_404(Tree, pk=pk)
    print(tree.image.url)
    return render(request, 'admin/tree_details_admin.html', {'tree': tree})

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
  return render(request, 'admin/tree_form.html', {'form': form})

@login_required(login_url='signin')  # Restrict access if needed
@staff_access_only()
def tree_update(request, pk):
  tree = Tree.objects.get(pk=pk)
  if request.method == 'POST':
    form = TreeForm(request.POST, request.FILES, instance=tree)  # Include request.FILES for image upload
    if form.is_valid():
      form.save()
      return redirect('tree_list')
  else:
    form = TreeForm(instance=tree)
  return render(request, 'admin/tree_form.html', {'form': form})

@login_required(login_url='signin')  # Restrict access if needed
def tree_delete(request, pk):
  tree = Tree.objects.get(pk=pk)
  tree.delete()
  return redirect('tree_list')


@login_required
def order(request):
    orders = OrderItem.objects.filter(user=request.user, ordered= False)
    previous_orders = Order.objects.filter(user=request.user)
    form= OrderForm()
    print("-----------------------")
    for i in orders:
       print(i.id)
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
    else:
        order_placed = Order.objects.filter(user=request.user,is_paid = False).first()
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
    previous_orders = Order.objects.filter(user=request.user)  

    context={
       'orders':orders,
       'previous_orders': previous_orders
    }
    
    return render(request, 'tree/order_item_form.html', context)


stripe.api_key= settings.STRIPE_SECRET_KEY

def order_payment_online(request, pk):
    
    return render(request,'tree/order_payment_online.html')

#@login_required
class create_checkout_session(View):
    def post(self, request, *args, **kwargs):
        DOMAIN = 'http://127.0.0.1:8000/'
        order_id= self.kwargs["pk"]
        order = Order.objects.get(id= order_id)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(order.price*100),
                        'product_data':{
                            'name': order.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
               'product_order_id': order.id
            },
            mode='payment',
            success_url= DOMAIN + 'success/',
            cancel_url= DOMAIN + 'cancel/',
        )
        return redirect(checkout_session.url, code=303)
    
def success(request):
    return render(request, 'tree/success.html')

def cancel(request):
    return render(request, 'tree/cancel.html')

endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  if (
    event['type'] == 'checkout.session.completed'
    or event['type'] == 'checkout.session.async_payment_succeeded'
  ):
    session = event['data']['object']
    customer_email = session['customer_details']['email']
    product_id = session['metadata']['product_order_id']
    order = get_object_or_404(Order, pk=int(product_id))
    order.is_paid = True
    order.save()

  return HttpResponse(status=200)



################################################################

'''
#ADMIN-------------
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'tree/order_list.html', {'orders': orders})
'''

#ADMIN-------------
@login_required
@staff_access_only()
def order_list(request):
    pending_orders = Order.objects.exclude(status ='Delivered')
    payment_update = Order.objects.filter(is_paid = False, status='Delivered')
    completed_orders = Order.objects.filter(is_paid = True, status='Delivered')
    context = {
       'pending_orders':pending_orders,
       'payment_update':payment_update,
       'completed_orders':completed_orders,
    }
    return render(request, 'admin/orders.html', context) 

#ADMIN-------------
@login_required
@staff_access_only()
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'tree/order_detail.html', {'orders': order})

#ADMIN-------------
@login_required
@staff_access_only()
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
def orders_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            # send email
            subject = 'Your Order Update on Treecommerce' 
            message = f"Dear {order.user.username},\nThis is an automated email regarding your recent order update.\nYour Order ID: {order.id}.\nYour current order status is: {order.status}.\nRegards,\nTreecommerce"

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [order.user.email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('order_list')
    else:
        form = UpdateOrderForm(instance=order)
    return render(request, 'admin/orders_details.html', {'form': form,'orders': order})

#ADMIN-------------
@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')