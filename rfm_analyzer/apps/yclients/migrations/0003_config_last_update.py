# Generated by Django 4.0.4 on 2022-04-16 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yclients', '0002_alter_config_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='last_update',
            field=models.DateTimeField(null=True),
        ),
    ]