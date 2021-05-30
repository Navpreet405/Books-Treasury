from json.decoder import JSONDecoder
from django.shortcuts import render, HttpResponse, redirect
import datetime
from .models import Contact, Seller, Cathome, Books, Review
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template import TemplateDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *

# Create your views here.
def index(request):
    category = request.GET.get('category')
    if category == None:
        books = Books.objects.all()
    else:
        books = Books.objects.filter(category__name=category)
    categories = Cathome.objects.all()
    context = {'categories':categories, 'books':books}

    return render(request, 'index.html', context)

    #return HttpResponse("this is homepage")

def about(request):
    category = request.GET.get('category')
    if category == None:
        books = Books.objects.all()
    else:
        books = Books.objects.filter(category__name=category)
    categories = Cathome.objects.all()
    context = {'categories':categories, 'books':books}

    return render(request, 'about.html', context)
   # return HttpResponse("this is about page")    

def reviews(request):
    if request.method == "POST":
        name = request.POST.get('name')
        bookName = request.POST.get('bookName')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        review = Review(name=name, bookName=bookName, phone=phone, desc=desc, date=datetime.datetime.today())
        review.save()
        messages.success(request, 'Congratulations! Your Review is added to our Database')

        #return redirect('home')
    return render(request, 'reviews.html')
    #return HttpResponse("this is reviews page")   

@login_required(login_url='/sign_in')
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        anyfile = request.FILES.get('anyfile')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, anyfile=anyfile, date=datetime.datetime.today())
        contact.save()

    return render(request, 'contact.html')
    #return HttpResponse("this is contact page")

def logoutUser(request):
    logout(request)
    return redirect('home')

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    return render(request, 'sign_in.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign_in')
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)

    context = {'form': form}
    return render(request, 'register.html', context)

def viewBook(request, pk):
    book = Books.objects.get(id=pk)
    messages.warning(request, 'You have to Login In to access Cart & e-Books')
    return render(request, 'book.html', {"book":book})
    #return HttpResponse("this is buy page")

#Changes made by MANISH
@login_required(login_url='/sign_in')
def sell(request):
    categories = Cathome.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        author = request.POST.get('author')
        phone = request.POST.get('phone')
        if request.POST.get('category'):
            savevalue=Seller()
            savevalue.category=request.POST.get('category')
            cate=savevalue.category
        
        category_new = request.POST.get('category_new')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        img = request.FILES.get('img')
        pdf = request.FILES.get('pdf')

        if cate != 'none':
            category = Cathome.objects.get(id=cate)
        elif category_new != '':
            category, created = Cathome.objects.get_or_create(name=category_new)
        else:
            category = None

        book = Books.objects.create(
            category=category,
            description=desc,
            image=img,
            name=name,
            price=price,
            pdf=pdf
        )

        seller = Seller(name=name, author=author, phone=phone, category=cate, price=price, desc=desc, img=img, date=datetime.datetime.today())
        seller.save()

        return redirect('home')

    context = {'categories':categories}
    return render(request, 'sell.html', context)


@login_required(login_url='/sign_in')
def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    product = Books.objects.get(id=productId)
    print(product)
    order, created = Order.objects.get_or_create(customer=request.user, complete=False)
    print(order)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    print(orderItem)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    print(orderItem.quantity)

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item is added", safe=False)

@login_required(login_url='/sign_in')
def checkout(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)

def proccessOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	order, created = Order.objects.get_or_create(customer=request.user, complete=False)


	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
            customer=request.user,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment Complete', safe=False)

def privacypolicy(request):
    return render(request, 'privacypolicy.html')

def terms(request):
    return render(request, 'terms.html')

def disclaimer(request):
    return render(request, 'disclaimer.html')

def misc(request):
    return render(request, 'misc.html')