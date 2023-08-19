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
        if not product.objects.all().filter(id = pro_id).exists():
            return redirect("allproducts")
        pro = product.objects.get(id=pro_id)
        if order_state:
            old_order = Order.objects.get(user=request.user , is_done=False)
            order_details = OrderDetails.objects.create(product=pro , order=old_order , price=pro.price , quantity=qty)
            messages.success(request, 'was is added To cart for old order')
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


def show_cart(request):
    context = None
    if request.user.is_authenticated and if not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user , is_done=False):
            order = Order.objects.get(user=request.user, is_done=False)
            order_details = OrderDetails.objects.all().filter(order=order)
            total_price = 0
            for item in order_details:
                total_price += item.price * item.quantity
            context = {
                    'order': order;
                    'order_details': order_details,
                    'total_price' : total_price,

                    }
    return render(request , "orders/show_cart.html" , context)




