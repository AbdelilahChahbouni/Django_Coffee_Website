from django.db import models
from django.contrib.auth.models import User
from allproducts.models import product
from django.utils import timezone
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    order_date = models.DateTimeField(default= timezone.now())
    details = models.ManyToMany(product , through= 'OrderDetails')
    is_done = models.BooleanField() 


    def __str__(self):
        return 'User : ' + self.user.username + ' , Order : ' + str(self.id)


class OrderDetails(models.Model):
    product = models.ForeignKey(product , on_delete = models.CASCADE)
    order = models.ForeignKey(Order , on_delete = models.CASCADE)
    price = models.DecimalField(max_digits=6 , decimal_places=2 )
    quantity = models.IntegerField()


    def __str__(self):
        return 'User : ' + self.order.user.username + ', Product : ' + self.product.name + ', Order_id : ' + str(self.order.id)




