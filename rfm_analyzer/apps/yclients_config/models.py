from django.db import models
from django.contrib.auth.models import User


class Config(models.Model):
    """ YClients connection configuration """

    class Meta:
        verbose_name = 'Configuration'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='yclients_config'
    )
    company_id = models.PositiveIntegerField()
    bearer_token = models.CharField(max_length=255)
    user_token = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.company_id)
