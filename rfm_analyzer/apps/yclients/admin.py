from django.contrib import admin

from rfm_analyzer.apps.yclients.forms import AddConfigAdminForm, ChangeConfigAdminForm
from rfm_analyzer.apps.yclients.models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    """ YClients connection configuration """

    list_display = ['user_name', 'user_email', 'company_id', 'last_update']

    def user_name(self, config):
        return config.user.username

    def user_email(self, config):
        return config.user.email

    def add_view(self, request, form_url='', extra_context=None):
        self.form = AddConfigAdminForm
        return super(ConfigAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.form = ChangeConfigAdminForm
        return super(ConfigAdmin, self).change_view(request, object_id, form_url, extra_context)
