from django.shortcuts import render,redirect
from store.models import Product
from .models import Cart,CartItem

############# Function for adding cart in session OR if already Available than fetching cart with same session_id.##############
def _card_id(request):  ############To make function private use_
    cart=request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
#################################################
def add_cart(request,product_id):
    current_user=request.user
    product=Product.objects.get(id=product_id)#get the product by matching product id in url
    ################For fetching cart object from database OR create new cart object if not Avilable in database#############
    try:
        cart=Cart.objects.get(cart_id=_card_id(request))#fetching cart from database that matches cart with sessionid _cart(request) is function
    except Cart.DoesNotExist:  
        cart=Cart.objects.create(       ####if cart does'nt found than creating cart object by Cart.objects.create
            cart_id=_card_id(request)
        )
        cart.save()    ###############saving cart in both scenerios.if Already exist  OR creating new cart
    ################For fetching cart object from database OR create new cart object if not Avilable in database Ends#############

    #############Now cartItem is created OR found & than add product in cartitem ###########
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity=+1##############Increasing cart item with one#########
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
        return redirect('cart')


def cart(request):
    return render(request,'store/cart.html')