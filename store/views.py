from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
# Create your views here.

def store(request,category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products_by_cat = Product.objects.filter(category=categories, is_available=True)
        # ===============paginator starts====
        paginator=Paginator(products_by_cat,3)
        page=request.GET.get('page')
        paged_by_products=paginator.get_page(page)
        # ============paginator ends===========
        product_count = products_by_cat.count()
    else:
        products_by_cat=Product.objects.filter(is_available=True).order_by('-id')
        product_count = products_by_cat.count()
        #For showing pagination in products
        # ===============paginator starts====
        paginator=Paginator(products_by_cat,3)
        page=request.GET.get('page')
        paged_by_products=paginator.get_page(page)
        # ============paginator ends===========

        
    context={
            'products':paged_by_products,
            'product_count': product_count,
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    product=get_object_or_404(Product,category__slug=category_slug, slug=product_slug)
    in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()##############Tocheck if product is in Already in cart
    context={
        'product':product,
        'in_cart':in_cart,
    }
    return render(request,'store/product_detail.html',context)


#============search functionality================
def search(request):
    if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                products = Product.objects.order_by('-id').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
                product_count = products.count()
                context = {
                    'products': products,
                    'product_count': product_count,
                }
            return render(request, 'store/store.html', context)