# Generated by Django 4.0.6 on 2022-08-15 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_campaign_voice_api_data_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='Description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]