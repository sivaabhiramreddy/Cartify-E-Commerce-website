from django.shortcuts import render, redirect
from .models import Product, Order, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('home')

    return render(request, 'register.html')

def home(request):
    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})


def cart(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render(request, 'cart.html', {'cart': cart, 'total': total})


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart = request.session.get('cart', [])

    cart.append({
        'name': product.name,
        'price': product.price
    })

    request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            address=address,
            total_price=total
        )

        request.session['cart'] = []
        return redirect('order_success')

    return render(request, 'checkout.html', {'total': total})


def remove_from_cart(request, index):
    cart = request.session.get('cart', [])

    if 0 <= index < len(cart):
        cart.pop(index)

    request.session['cart'] = cart
    return redirect('cart')


def order_success(request):
    return render(request, 'order_success.html')