from django.db import models
from .base import InteractionBase
from django.core.exceptions import ValidationError



class Follow(InteractionBase):
    ACTOR_TYPE = [
        ('user', 'User'),

        ('university', 'University'),
        ('industry', 'Industry'),
        ('business', 'Business'),
        
        # ('individual', 'Individual'),
    ]
    TARGET_TYPE = [
        ('user', 'User'),

        ('university', 'University'),
        ('industry', 'Industry'),
        ('business', 'Business'),

        ('product', 'Product'),
        ('service', 'Service'),
        
        # ('comment', 'Comment'),
        # ('individual', 'Individual'),
    ]

    ACTOR_TYPE_ENUM_FOLLOW_PARAM = [choice[0] for choice in ACTOR_TYPE]
    TARGET_TYPE_ENUM_FOLLOW_PARAM = [choice[0] for choice in TARGET_TYPE]

    actor_type = models.CharField(max_length=50, choices=ACTOR_TYPE)
    actor_id = models.CharField(max_length=100)
    target_type = models.CharField(max_length=50, choices=TARGET_TYPE)
    target_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def clean(self):
    #     # چک محدودیت actor_type
    #     if self.actor_type not in ActorType.values:
    #         raise ValidationError("فقط user و service_provider می‌توانند actor شوند.")
    #     # چک محدودیت target_type
    #     if self.target_type == 'comment':
    #         raise ValidationError("comment نمی‌تواند target فالو باشد.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    

    class Meta:
        db_table = "interactive_follow"
        unique_together = ("actor_type", "actor_id", "target_type", "target_id")
        indexes = [
            models.Index(fields=["actor_type", "actor_id"]),
            models.Index(fields=["target_type", "target_id"]),
        ]

    def __str__(self):
        return f"{self.actor_type}:{self.actor_id} -> {self.target_type}:{self.target_id}"