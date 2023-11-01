from django.shortcuts import render , get_object_or_404
from datetime import datetime
from .models import product as myproduct
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
# Create your views here.


def allproducts(request):
    prod = myproduct.objects.all()
    # configure Paginator stack
    page = request.GET.get('page', 1)
    paginator = Paginator(prod, 2)
    cs = None
    if "cs_state" in request.GET:
        cs = request.GET["cs_state"]
        if not cs:
            cs = "off"
    if "search_name" in request.GET:
        name = request.GET["search_name"]
        if name:
            if cs == "on":
                prod = prod.filter(name__contains=name)
            else:
                prod = prod.filter(name__icontains=name)

        
    if "search_desc" in request.GET:
        desc = request.GET["search_desc"]
        if desc:
            if cs == "on":
                prod = prod.filter(name__contains=desc)
            elif cs == "off":
                prod = prod.filter(name__icontains=name)

    if "search_priceto" in request.GET and "search_pricefrom" in request.GET:
        pfrom = request.GET["search_pricefrom"]
        pto = request.GET["search_priceto"]
        if pfrom and pto:
            if pfrom.isdigit() and pto.isdigit():
                prod = prod.filter(price__gte=pfrom , price__lte=pto)

    
    try:
        prod = paginator.page(page)
    except PageNotAnInteger:
        prod = paginator.page(1)
    except EmptyPage:
        prod = paginator.page(paginator.num_pages)




    data = {'products': prod }
    return render(request,'allproducts/allproducts.html',data )


def product(request , pro_id):
    data = {'prod':  get_object_or_404(myproduct , pk=pro_id)}
    return render(request , 'allproducts/product.html' , data)


def search(request):
    return render(request , 'allproducts/search.html')
