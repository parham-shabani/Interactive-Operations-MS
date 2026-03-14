from django.db import models
# from .base import ActorType
from core.enums import ActorType


class Like(models.Model):
    ACTOR_TYPE = [
        ('user', 'User'),
        ('business', 'Business'),
        ('university', 'University'),
        ('industry', 'Industry'),
    ]
    TARGET_TYPE = [
        ('user', 'User'),

        ('business', 'Business'),
        ('university', 'University'),
        ('industry', 'Industry'),

        ('product', 'Product'),
        ('service', 'Service'),
        
        ('comment', 'Comment'),
    ]
    LIKE_STATUS= [
        ('NONE', 'هیچکدام'),
        ('LIKE', 'لایک'),
        ('DISLIKE', 'دیسلایک'),
    ]

    ACTOR_TYPE_ENUM_LIKE_PARAM = [choice[0] for choice in ACTOR_TYPE]
    TARGET_TYPE_ENUM_LIKE_PARAM = [choice[0] for choice in TARGET_TYPE]

    actor_type = models.CharField(max_length=50, choices=ACTOR_TYPE)
    actor_id = models.CharField(max_length=100)
    target_type = models.CharField(max_length=50, choices=TARGET_TYPE)
    target_id = models.CharField(max_length=100)
    like_status = models.CharField(max_length=10, choices=LIKE_STATUS, default='LIKE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['actor_type', 'actor_id', 'target_type', 'target_id']]
        indexes = [
            models.Index(fields=['target_type', 'target_id', 'like_status']),
            models.Index(fields=['actor_type', 'actor_id', 'like_status']),
        ]
    
    def __str__(self):
        return f"{self.actor_type}:{self.actor_id} → {self.target_type}:{self.target_id}: {self.like_status}"
