import json
from .models import *


def cookieCart(request):
        try:                                                        # this error will come when we try to load cart.html qithout loading the main page, we dont have cookies which will be generated in the previous sessions
            cart = json.loads(request.COOKIES['cart'])               #Getting the cookie from the front end of the page that has been set in main.html
        except:
            cart={}
                                                             # creating an empty dictionary if their is no cookie from the main.html file
        print('Anonymous User : Cart : ',cart)
        items=[]
        order ={'get_cart_total':0,'get_cart_quantity':0,'shipping':False}
        cartItems = order['get_cart_quantity']

        for item_id in cart:
            #We  use  try block to prevent items in cart that may benn removed may cause an exception becuas equering an item that does not exit in the database will throw an error
            try:
                cartItems += cart[item_id]['quantity']                   #getting the quantity of the products in the cart

                product = Product.objects.get(id=item_id)                  #We have the id of the product and we get the product object by quering the product
                total_product = (product.price * cart[item_id]['quantity'])

                order['get_cart_total'] += total_product  # total of each item
                order['get_cart_quantity'] += cart[item_id]['quantity']
                item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity': cart[item_id]['quantity'],
                'get_total':total_product
                }
                items.append(item)

                if product.digital == False:
                    order["shipping"]=True
            except Exception as e:
                print('The product does not exit , might be removed from the database')

        return {'items': items,'order':order,'cartItems':cartItems}












def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'items': items,'order':order,'cartItems':cartItems}




def guestOrder(request,data):

    print('User is not autheticated')

    print('COOKIES : ',request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']


    customer ,created = Customer.objects.get_or_create(email=email,)
    # here email is the primary key and we are assigning the name to the customer outside get_or_create
    # because the user can change their name later , email is unique identifier for the customer
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer,complete=False,)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(product=product,order=order,quantity=item['quantity'])

    return customer ,order
