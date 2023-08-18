from django.shortcuts import render , redirect
from .models import Order , OrderDetails
from allproducts.models import product
from django.utils import timezone
from django.contrib import messages

# Create your views here.

def add_to_cart(request):
    if 'pro_id' in request.GET and 'price' in request.GET and 'qty' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET['pro_id']
        qty = request.GET['qty']
        order_state = Order.objects.all().filter(user=request.user, is_done=False)
        pro = product.objects.get(id=pro_id)
        if order_state:
            messages.success(request, 'this order is done')
        else:
            new_order = Order()
            new_order.user = request.user
            new_order.order_date = timezone.now()
            new_order.is_done = False
            new_order.save()

            order_datails = OrderDetails.objects.create(product=pro , order=new_order , price=pro.price , quantity=qty)
        






            messages.success(request, 'this order will be done')

        return redirect('/allproducts/' + request.GET['pro_id'])

    else:
        return redirect("allproducts")







