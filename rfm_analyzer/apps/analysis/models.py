from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    phone = models.PositiveBigIntegerField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)


class Week(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # All data from data providers (YClients) is stored with local dates.
    # But last_update field is stored with UTC, as it recomended.
    since = models.DateField()
    till = models.DateField()
    visits = models.PositiveIntegerField(default=0)
    payed = models.DecimalField(max_digits=9, decimal_places=2, default=0)
