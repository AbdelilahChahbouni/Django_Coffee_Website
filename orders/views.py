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
            if OrderDetails.objects.all().filter(order=old_order , product=pro):
                order_detail = OrderDetails.objects.get(order=old_order,product=pro)
                order_detail.quantity += int(qty)
                order_detail.save()
            else:
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
        if 'pro_id' in request.GET:
            messages.error(request,"You must be logged in")
            return redirect("/allproducts/" + request.GET["pro_id"])

        else:
            return redirect("index")


def show_cart(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user , is_done=False):
            order = Order.objects.get(user=request.user, is_done=False)
            order_details = OrderDetails.objects.all().filter(order=order)
            total_price = 0
            for item in order_details:
                total_price += item.price * item.quantity
            context = {
                    'order': order,
                    'order_details': order_details,
                    'total_price' : total_price,

                    }
    return render(request , "orders/show_cart.html" , context)


def remove_from_cart(request , orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        removed_order = OrderDetails.objects.get(id=orderdetails_id)
        if removed_order.order.user.id == request.user.id:
            removed_order.delete()
        return redirect("show_cart")


def add_qty(request , orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        my_orderdetails =OrderDetails.objects.get(id=orderdetails_id)
        if my_orderdetails.order.user.id == request.user.id:
            my_orderdetails.quantity += 1
            my_orderdetails.save()
    return redirect("show_cart")



def sub_qty(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails =OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            if orderdetails.quantity > 1:
                orderdetails.quantity -= 1
                orderdetails.save()
    return redirect("show_cart")



def payment(request):
    context = None
    ship_address = None
    ship_phone = None
    code_number = None
    expire = None
    security_code = None

    if request.method =='POST' and 'btn-payment' in request.POST:
        

        context = {
            'ship_address' : ship_address,
            'ship_phone' : ship_phone,
            'code_number' : code_number,
            'expire' : expire,
            'security_code' : security_code,
        }


    else request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user , is_done=False):
            order = Order.objects.get(user=request.user, is_done=False)
            order_details = OrderDetails.objects.all().filter(order=order)
            total_price = 0
            for item in order_details:
                total_price += item.price * item.quantity
            context = {
                    'order': order,
                    'order_details': order_details,
                    'total_price' : total_price,

                    }
    return render(request , "orders/payment.html" , context)
