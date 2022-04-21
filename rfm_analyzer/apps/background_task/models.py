from django.db import models
from django.contrib.auth.models import User

class BackgroundTask(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
