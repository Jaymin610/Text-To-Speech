from django.db import models

# Create your models here.

class User1(models.Model):
    email = models.EmailField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=10, blank=True, null=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    otp = models.CharField(max_length=6, default=359)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)


class Campaign(models.Model):
    user_key = models.ForeignKey(User1, on_delete=models.CASCADE, null=True)
    CampaignName = models.CharField(max_length = 255,null=True,blank=True)
    CampaignStatus = models.CharField(max_length=255, null=True, blank=True)

class Services(models.Model):
    campaign_key = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    ServiceName = models.CharField(max_length = 255,null=True,blank=True)
