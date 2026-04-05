# InteractiveOperations/models/like.py
from django.db import models
from .base_like import AbstractLikeBase

class UserLikeUser(AbstractLikeBase):
    class Meta:
        db_table = "interactive_user_like_user"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserLikeServiceProvider(AbstractLikeBase):
    class Meta:
        db_table = "interactive_user_like_service_provider"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserLikeOthers(AbstractLikeBase):
    class Meta:
        db_table = "interactive_user_like_others"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderLikeUser(AbstractLikeBase):
    class Meta:
        db_table = "interactive_sp_like_user"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderLikeServiceProvider(AbstractLikeBase):
    class Meta:
        db_table = "interactive_sp_like_sp"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderLikeOthers(AbstractLikeBase):
    class Meta:
        db_table = "interactive_sp_like_others"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]