from django.contrib import admin

from rfm_analyzer.apps.yclients.forms import ConfigAdminForm
from rfm_analyzer.apps.yclients.models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    """ YClients connection configuration """

    list_display = ['user_name', 'user_email', 'company_id', 'last_update']
    form = ConfigAdminForm

    def user_name(self, config):
        return config.user.username

    def user_email(self, config):
        return config.user.email
