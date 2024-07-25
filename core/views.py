from django.shortcuts import render, redirect
from django.views import View
from core.models import (
    Product,
    Customer,
    Cart,
    OrderPlaced
)
from django.http import JsonResponse
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import uuid



# Class Based Views

class HomePageView(View):
    def get(self, request):
        mobile_phones = Product.objects.filter(category="M")
        head_phones = Product.objects.filter(category="H")

        context = {'mobiles': mobile_phones, 'headphones': head_phones}
        return render(request, "index.html", context)
    
class ProduceDetailView(View):
    def get(self, request, pk=None):
        print(f"id: pk")
        current_product = Product.objects.get(id=pk)
        item_in_cart = False
        if request.user.is_authenticated:
            item_in_cart = Cart.objects.filter(Q(product=current_product.id) & Q(user=request.user)).exists()
            
        context = {'product': current_product, 'item_in_cart': item_in_cart}
        return render(request, "product_detail.html", context)
    
class AboutPageView(View):
    def get(self, request):
        context = {}
        return render(request, "about.html", context)
    
class ContactPageView(View):
    def get(self, request):
        context = {}
        return render(request, "contact.html", context)
    
login_required(login_url="/auth/login/")
class AddToCartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            product_id = request.GET['prod_id']
            product_instance = Product.objects.get(id=product_id)

            cart = Cart(user=user, product=product_instance)
            cart.save()

            print(f"id is: {product_id}")
            return redirect('show_cart')
        else:
            return redirect('login-view')
        
# function for price calculation
@login_required(login_url="/auth/login/")
def price_calculation(request):
        amount = 0.0
        shipping_amount = 40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        # print(f"inside cart_product: {cart_product}")

        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
        data = {'amount': amount, 'total_amount': amount + shipping_amount, }
        return data

        
# function based view  for showing cart items
login_required(login_url='/auth/login/')
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        # print(f"inside cart: {cart}")
        amount = 0.0
        shipping_amount = 40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(f"inside cart_product: {cart_product}")

        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
                total_amount = amount + shipping_amount

            return render(request, "add_to_cart.html", {'carts': cart, 'total_amount': total_amount, 'amount': amount, 'shipping_amount': shipping_amount})
        else:
            return render(request, "empty_cart.html", {'msg': 'Cart is Empty!'})
    else:
        return redirect('login-view')
    

# function based view for pluscart
login_required(login_url="/auth/login/")
def plus_cart_view(request):
    if request.method == "GET":
        product_id = request.GET['product_id']
        # print(f"pid: {product_id}")
        current_cart = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        current_cart.quantity += 1
        current_cart.save()

        data = price_calculation(request)
        data['quantity'] = current_cart.quantity

        return JsonResponse(data)
    
# function based view for minuscart
login_required(login_url="/auth/login/")
def minus_cart_view(request):
    if request.method == "GET":
        product_id = request.GET['product_id']
        # print(f"pid: {product_id}")
        current_cart = Cart.objects.get(Q(product=product_id) & Q(user = request.user))
        current_cart.quantity -= 1
        current_cart.save()
        data = price_calculation(request)
        data['quantity'] = current_cart.quantity

        return JsonResponse(data)
    
# function based view for removing cart
login_required(login_url="/auth/login/")
def remove_cart_view(request):
    if request.method  == "GET":
        product_id = request.GET['product_id']
        # print(f"pid: {product_id}")
        current_cart = Cart.objects.get(Q(product=product_id) & Q(user = request.user))
        current_cart.delete()
        data = price_calculation(request)

        return JsonResponse(data)
    
import hashlib 
import hmac
import base64

def generate_hash(cost, uuid, paycode):
    # Convert inputs to strings
    cost_str = str(cost)
    uuid_str = str(uuid)
    paycode_str = str(paycode)

    # Convert strings to bytes using UTF-8 encoding
    cost_bytes = cost_str.encode('utf-8')
    uuid_bytes = uuid_str.encode('utf-8')
    paycode_bytes = paycode_str.encode('utf-8')

    # Generate HMAC using SHA256 algorithm
    hash_object = hmac.new(cost_bytes + uuid_bytes + paycode_bytes, digestmod=hashlib.sha256)

    # Get the digest and encode it in base64
    hash_in_base64 = base64.b64encode(hash_object.digest()).decode()

    return hash_in_base64

# generate uuid
import uuid
import random
def generate_transaction_uuid():
    # Generate random numbers for each part
    first_part = str(random.randint(10, 99))  # Generate a random number between 10 and 99
    second_part = str(random.randint(100, 999))  # Generate a random number between 100 and 999
    third_part = str(random.randint(10, 99))  # Generate a random number between 10 and 99

    # Combine the parts with hyphens
    transaction_uuid = "-".join([first_part, second_part, third_part])

    return transaction_uuid





# class based view for checkout
# @method_decorator(login_required(login_url="/auth/login/"), name="dispatch")
class checkout_view(View):
    def get(self, request):
        user = request.user
        address = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user = user)
        # Calculate total cost for each cart item
        total_costs = [cart_item.total_cost for cart_item in cart_items]
        print(f"tc: {total_costs[0]} type:{type(total_costs[0])}")



        unique_id = generate_transaction_uuid()

        secret_key = "8gBm/:&EnhH.1/q"

        strings = [f"{total_costs[0]}", f"{unique_id}", "EPAYTEST"]
        hash_data = "".join(strings)
        print(hash_data)

        result = generate_hash(total_costs[0], unique_id, "EPAYTEST")

        data = price_calculation(request)
        data['address'] = address
        data['cart_items'] = cart_items
        data['unique_id']  = unique_id
        data['secret_key'] = secret_key
        data['signature'] = result


        return render(request, 'checkout.html', data)
    

    
# class based view for payment done
@method_decorator(login_required(login_url="/auth/login/") , name="dispatch")
class payment_done_view(View):
    def get(self, request):
        user = request.user
        custid = request.GET.get('custid')
        print(f"id is: {custid}")
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            order = OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity)
            order.save()
            c.delete()
        context = {}
        return redirect("order_placed")
    

# class based view for order placed
method_decorator(login_required(login_url="/auth/login/") , name="dispatch")
class order_placed_view(View):
    def get(self, request):
        user = request.user
        op = OrderPlaced.objects.filter(user=user)

        context = {'order_placed': op, 'customer': user}
        return render(request, "order_placed.html", context)

        



    
        

