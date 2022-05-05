from django.db import models
from django.contrib.auth.models import User


class Config(models.Model):
    """ YClients connection configuration """

    class Meta:
        verbose_name = 'Connection configuration'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='yclients_config'
    )
    company_id = models.PositiveIntegerField()
    bearer_token = models.CharField(max_length=255)
    user_token = models.CharField(max_length=255)
    # All data from data providers (YClients) is stored with local dates.
    # But last_update field is stored with UTC, as it recomended.
    last_update = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.company_id)
