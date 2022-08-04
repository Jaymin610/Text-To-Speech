# Generated by Django 4.0.6 on 2022-08-03 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_data_summary_upload_req_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_summary',
            name='upload_req',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='data_summary',
            name='upload_res',
            field=models.JSONField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='data_summary',
            name='voiceshoot_req',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='data_summary',
            name='voiceshoot_res',
            field=models.JSONField(blank=True, max_length=255, null=True),
        ),
    ]
