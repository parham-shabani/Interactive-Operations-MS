from django.db import models
from core.enums import ActorType

class SharePlatform(models.TextChoices):
    IN_SITE = 'in_site', 'درون سایت'
    TELEGRAM = 'telegram', 'تلگرام'
    WHATSAPP = 'whatsapp', 'واتساپ'


# class ShareMethod(models.TextChoices):
#     IN_SITE = 'in_site', 'درون سایت'
#     EXTERNAL_APP = 'external_app', 'اپ دیگر'


class Share(models.Model):
    actor_type = models.CharField(max_length=20, choices=ActorType.choices)
    actor_id = models.CharField(max_length=100)
    target_type = models.CharField(max_length=20, choices=ActorType.choices)
    target_id = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=SharePlatform.choices)
    destination_type = models.CharField(max_length=20, choices=ActorType.choices, null=True, blank=True)
    destination_id = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(default='')
    #should change it later   i changed it at 09/11/1404   tavasote app url page gharar migirad
    reason = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
