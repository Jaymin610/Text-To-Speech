# Generated by Django 4.0.6 on 2022-08-02 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_data_summary_delete_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_summary',
            name='API_Type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
