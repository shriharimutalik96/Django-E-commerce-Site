from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from . utils import cookieCart,cartData

# Create your views here.


def store(request):

    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order,created = Order.objects.get_or_create(customer=customer,complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_quantity
    # else:
    #     # Create an empty cart for non logged in user
    #     # Accepting the cookies from the front end of the wbsite, that will be sent from the frontend(JS) the backend in the form of JSON objects , we need to load them all first
    #     cookieData = cookieCart(request)
    #     cartItems = cookieData['cartItems']

    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context ={'products': products,'cartItems':cartItems}
    return render(request,'store/store.html',context)




# A view for updating the cart
def cart(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order,created = Order.objects.get_or_create(customer=customer,complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_quantity
    # else:
    #     cookieData = cookieCart(request)
    #     cartItems = cookieData['cartItems']
    #     order = cookieData['order']
    #     items = cookieData['items']

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context={'items': items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context,)







def checkout(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order,created = Order.objects.get_or_create(customer=customer,complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_quantity
    # else:
    #     cookieData = cookieCart(request)
    #     cartItems = cookieData['cartItems']
    #     order = cookieData['order']
    #     items = cookieData['items']

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)





def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action : ',action)
    print('Product  Id :',productId)

    customer = request.user.customer                                                      # getting the customer from the request object
    product = Product.objects.get(id=productId)                                            # getting the info about the product using Product ID
    order,created = Order.objects.get_or_create(customer=customer,complete=False)           #creating an order using customer obj
    orderItem , created_item = OrderItem.objects.get_or_create(order=order,product=product)      #create an order item obj


    if action=='add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action=='remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save() # saving the order item to the database

    if orderItem.quantity <=0:  # if the order item is less than zero then remove that thing from the database
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)
#In order to allow non-dict objects to be serialized set the safe parameter to False.




# @csrf_exempt
def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)             # Sending data from front end of the website

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShipppingAddress.objects.create(
                customer = customer,
                order = order,
                address =data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipCode'],
                country = data['shipping']['country'])

    else:
        print('User is not autheticated , send them back to login or signup')

    return JsonResponse('Payment Completed',safe=False)
