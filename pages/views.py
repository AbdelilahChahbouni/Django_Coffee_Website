from django.shortcuts import render
from django.http import HttpResponse
from allproducts.models import product
# Create your views here.

def index(request):
    #data = {"products": product.objects.all()[:6]}
    data = {"products" : product.objects.all() }
    return render(request , 'pages/index.html' , data)


def about(request):
    return render(request , 'pages/about.html')

def coffee(request):
    return render(request , 'pages/coffee.html')
