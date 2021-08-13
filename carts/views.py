from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Cart,CartItem

############# Function for adding cart in session OR if already Available than fetching cart with same session_id.##############
def _cart_id(request):  ############To make function private use_
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
        cart=Cart.objects.get(cart_id=_cart_id(request))#fetching cart from database that matches cart with sessionid _cart(request) is function
    except Cart.DoesNotExist:  
        cart=Cart.objects.create(       ####if cart does'nt found than creating cart object by Cart.objects.create
            cart_id=_cart_id(request)
        )
    cart.save()    ###############saving cart in both scenerios.if Already exist  OR creating new cart
    ################For fetching cart object from database OR create new cart object if not Avilable in database Ends#############

    #############Now cartItem is created OR found & than add product in cartitem ###########
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity  += 1##############Increasing cart item with one#########
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')

###########decrement product from cart################
def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))#fetching cart from database that matches cart with sessionid _cart(request) is function
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

###########Remove product from cart After clicking Remove button################
def remove_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))#fetching cart from database that matches cart with sessionid _cart(request) is function
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


#################View to fetching cart items to specific session ID#############
def cart(request,total=0,quantity=0,cart_items=None,):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))############It will fetch cart from database matching cart session id####
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:##############This loop will fetch all specific cart items from specific cart
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass   ###########Do Nothing############

    context={
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'tax'     :tax,
        'grand_total':grand_total,
    }
    return render(request,'store/cart.html',context)


    
