# Generated by Django 4.0.6 on 2022-08-15 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_campaign_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='record_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]