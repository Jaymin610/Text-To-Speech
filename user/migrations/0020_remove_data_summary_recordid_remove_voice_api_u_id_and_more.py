# Generated by Django 4.0.6 on 2022-08-10 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_alter_data_summary_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data_summary',
            name='recordID',
        ),
        migrations.RemoveField(
            model_name='voice_api',
            name='u_ID',
        ),
        migrations.DeleteModel(
            name='Campaign',
        ),
        migrations.DeleteModel(
            name='Data_Summary',
        ),
        migrations.DeleteModel(
            name='Voice_API',
        ),
    ]
