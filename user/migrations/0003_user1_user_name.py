# Generated by Django 4.0.6 on 2022-07-27 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user1_otp_remove_user1_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user1',
            name='user_name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
