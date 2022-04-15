from django.contrib import admin

from . models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    """ YClients connection configuration """

    class Meta:
        verbose_name = 'Some other name'

    list_display = ['user_name', 'user_email', 'company_id',
                    'bearer_token', 'user_token']

    def user_name(self, config):
        return config.user.username

    def user_email(self, config):
        return config.user.email
