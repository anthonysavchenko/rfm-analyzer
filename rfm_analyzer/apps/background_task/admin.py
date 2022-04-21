from django.contrib import admin

from rfm_analyzer.apps.background_task.models import BackgroundTask


@admin.register(BackgroundTask)
class BackgroundTaskAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_email', 'created']

    def user_name(self, background_task):
        return background_task.user.username

    def user_email(self, background_task):
        return background_task.user.email
