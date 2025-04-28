from django.shortcuts import render
from .models import products
# Create your views here.

def Product(request):
    return render(request,'products/product.html')


def Products(request):
    return render(request,'products/products.html', {'pro':products.objects.all()})