# Generated by Django 4.0.6 on 2022-08-02 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user1_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data_Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(blank=True, max_length=10)),
                ('text', models.CharField(blank=True, max_length=255, null=True)),
                ('speechFile', models.CharField(blank=True, max_length=50, null=True)),
                ('recordID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.campaign')),
            ],
        ),
        migrations.DeleteModel(
            name='Services',
        ),
    ]