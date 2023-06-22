from django.urls import path
from . import views




urlpatterns = [
        path('' , views.allproducts , name= 'allproducts'),
        path('<int:pro_id>' , views.product , name='product'),
        path('search' , views.search , name='search'),
        ]
