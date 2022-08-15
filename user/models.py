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


class Voice_API(models.Model):
    u_ID = models.ForeignKey(User1, on_delete=models.CASCADE, null=True)
    voice_API = models.CharField(max_length=255, blank=True, null=True)
    domain = models.CharField(max_length=255, blank=True, null=True)
    u_name = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    plan = models.CharField(max_length=255, blank=True, null=True)
    caller_id = models.CharField(max_length=255, blank=True, null=True)
    upload_url = models.CharField(max_length=255, blank=True, null=True)
    voiceshoot_url = models.CharField(max_length=255, blank=True, null=True)


class Campaign(models.Model):
    user_key = models.ForeignKey(User1, on_delete=models.CASCADE, null=True)
    CampaignName = models.CharField(max_length=255, null=True, blank=True)
    Description = models.CharField(max_length=255, null=True, blank=True)
    record_count = models.IntegerField(null=True, blank=True)
    CampaignStatus = models.CharField(max_length=255, null=True, blank=True)


class Data_Summary(models.Model):
    recordID = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=10, null=False, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    speechFile = models.CharField(max_length=50, null=True, blank=True)
    TTS_Provider = models.CharField(max_length=50, null=True, blank=True)
    Voice_API = models.CharField(max_length=50, null=True, blank=True)
    upload_req = models.CharField(max_length=255, null=True, blank=True)
    upload_res = models.JSONField(max_length=255, null=True, blank=True)
    voiceshoot_req = models.CharField(max_length=255, null=True, blank=True)
    voiceshoot_res = models.JSONField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, default="Pending")
