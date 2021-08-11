from django.shortcuts import render
from store.models import Product

# Create your views here.

def home(request):
    product=Product.objects.filter(is_popular=True,is_available=True).order_by('-created_date')

    context={
        'products':product
    }
    return render(request,'home.html',context)
    
