from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    phone = models.PositiveBigIntegerField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)


class Week(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    since = models.DateField()
    till = models.DateField()
    visits = models.PositiveIntegerField(default=0)
    payed = models.DecimalField(max_digits=9, decimal_places=2, default=0)
