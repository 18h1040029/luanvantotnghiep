
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from . utils import cookieCart, cartData, guestOrder
from django.contrib.auth.forms import UserCreationForm
# Create your views here
from .forms import  CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import random
# API TEST
from rest_framework import viewsets
from .serializers import storeSerializer

class storeViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = storeSerializer

def store(request):

	Data= cartData(request)
	cartItems = Data['cartItems']
	print(cartItems)
	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def product_detail(request,id):
    Data= cartData(request)
    product=Product.objects.get(id=id)
    cartItems = Data['cartItems']
    context = {'product':product,'cartItems':cartItems}
    return render(request, 'store/product_detail.html', context)



def main(request):

	if request.user.is_authenticated:
		user= request.user
	context = {'user':user,}
	return render(request, 'store/main.html', context)

def orderHistory(request):
	user= request.user
	customer=request.user.customer
	# all_orders = Order.objects.filter(customer=customer)
	# orders = all_orders.order_by('-id')
	orders= Order.objects.filter(customer=customer).order_by('-id')[1:]
	context = { 'orders':orders}
	print(orders)
	return render(request, 'store/order_history.html', context)

def my_orders(request,id):
    order=Order.objects.get(id=id)
    items=order.orderitem_set.all()
    context={"items":items}
    return render(request,'store/my_orders.html',context)

def logoutUser(request):
    
    logout(request)
    return redirect('login')


def cart(request):

	
	Data= cartData(request)
	cartItems = Data['cartItems']
	order = Data['order']
	items = Data['items']
		
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	Data= cartData(request)
	cartItems = Data['cartItems']
	order = Data['order']
	items = Data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request,data)

	total = float(data['form']['total'])
	order.transaction_id= transaction_id
 
	if total == float(order.get_cart_total):
		order.complete=True
	order.save()
 
	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
	)
	return JsonResponse('Payment submitted..', safe=False)


def registerPage(request):
	form=CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			
			email = form.cleaned_data.get('email')
			
			u, created = User.objects.get_or_create(username=user, email=email)
			if created:
				raise Exception()
			messages.success(request,'Tài khoản '+user+' đã được tạo thành công')
			customer,created = Customer.objects.get_or_create(
				user=u,
			)
			customer.name=user
			customer.email=email
			customer.is_active= True
			customer.save()
			x=Customer.objects.all()
			
			return redirect('login')
			
   
   
	context={"form":form}
	return render(request, 'store/register.html', context)

def loginPage(request):
	if request.method =='POST':
		username= request.POST.get('username') 
		password= request.POST.get('password')
		user = authenticate(request, username = username , password= password)
		if user is not None:
			login(request, user)
			return redirect('store')

	context ={}
	return render(request, 'store/login.html', context)



