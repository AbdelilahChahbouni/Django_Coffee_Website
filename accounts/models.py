from django.db import models
from django.contrib.auth.models import User
from allproducts.models import product
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    product_favorite = models.ManyToManyField(product)

    address = models.CharField(max_length=60)
    address2 = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    zip_number = models.CharField(max_length=5)

    def __str__(self):
        return self.user.username



