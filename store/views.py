from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from category.models import Category
# Create your views here.

def store(request,category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products_by_cat = Product.objects.filter(category=categories, is_available=True)
        product_count = products_by_cat.count()
    else:
        products_by_cat=Product.objects.filter(is_available=True).order_by('-created_date')
        product_count = products_by_cat.count()

        
    context={
            'products':products_by_cat,
            'product_count': product_count,
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    product=get_object_or_404(Product,category__slug=category_slug, slug=product_slug)
    context={
        'product':product
    }
    return render(request,'store/product_detail.html',context)