from django.db import models

# Create your models here.

class User1(models.Model):
    user_name = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=10, blank=True, null=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)


class Campaign(models.Model):
    user_key = models.ForeignKey(User1, on_delete=models.CASCADE, null=True)
    CampaignName = models.CharField(max_length = 255,null=True,blank=True)
    CampaignStatus = models.CharField(max_length=255, null=True, blank=True)


class Data_Summary(models.Model):
    recordID = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=10, null=False, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    speechFile = models.CharField(max_length=50, null=True, blank=True)
    API_Type = models.CharField(max_length=50, null=True, blank=True)
    upload_req = models.CharField(max_length=255, null=True, blank=True)
    upload_res = models.JSONField(max_length=255, null=True, blank=True)
    voiceshoot_req = models.CharField(max_length=255, null=True, blank=True)
    voiceshoot_res = models.JSONField(max_length=255, null=True, blank=True)

