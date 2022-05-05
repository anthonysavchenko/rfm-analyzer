from django.forms import ModelForm, PasswordInput

from .models import Config


class AddConfigAdminForm(ModelForm):
    class Meta:
        model = Config
        fields = ('user', 'company_id', 'bearer_token', 'user_token')
        widgets = {
            'bearer_token': PasswordInput(),
            'user_token': PasswordInput(),
        }


class ChangeConfigAdminForm(ModelForm):
    class Meta:
        model = Config
        fields = ('user', 'last_update')
