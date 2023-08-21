from django.urls import path
from . import views



urlpatterns = [
        path("add_to_cart" , views.add_to_cart , name='add_to_cart'),
        path("show_cart" , views.show_cart , name="show_cart"),
        path("<int:orderdetails_id>" , views.remove_from_cart , name="remove_from_cart"),
        ]

