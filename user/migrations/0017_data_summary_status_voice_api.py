# Generated by Django 4.0.6 on 2022-08-05 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_user1_voice_api'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_summary',
            name='status',
            field=models.BooleanField(default=0),
        ),
        migrations.CreateModel(
            name='Voice_API',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voice_API', models.CharField(blank=True, max_length=255, null=True)),
                ('upload_url', models.CharField(blank=True, max_length=255, null=True)),
                ('voiceshoot_url', models.CharField(blank=True, max_length=255, null=True)),
                ('u_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user1')),
            ],
        ),
    ]