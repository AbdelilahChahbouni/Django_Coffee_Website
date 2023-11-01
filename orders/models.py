from django.db import models
from django.contrib.auth.models import User
from allproducts.models import product
from django.utils import timezone
from creditcards.models import CardNumberField , CardExpiryField , SecurityCodeField
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    order_date = models.DateTimeField(default= timezone.now())
    details = models.ManyToManyField(product , through= 'OrderDetails')
    is_done = models.BooleanField() 
    total = 0
    items_counter = 0


    def __str__(self):
        return 'User : ' + self.user.username + ' , Order : ' + str(self.id)


class OrderDetails(models.Model):
    product = models.ForeignKey(product , on_delete = models.CASCADE)
    order = models.ForeignKey(Order , on_delete = models.CASCADE)
    price = models.DecimalField(max_digits=6 , decimal_places=2 )
    quantity = models.IntegerField()


    def __str__(self):
        return 'User : ' + self.order.user.username + ', Product : ' + self.product.name + ', Order_id : ' + str(self.order.id)

    class Meta:
        ordering= ["id"]


        

class Payment(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    shipment_address = models.CharField(max_length=200)
    shipment_phone = models.CharField()
    card_number = CardNumberField()
    expire = CardExpiryField()
    security_code = SecurityCodeField()

    
