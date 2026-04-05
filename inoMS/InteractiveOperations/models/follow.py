from django.db import models
from .base_follow import AbstractFollowBase

class UserFollowUser(AbstractFollowBase):
    class Meta:
        db_table = "interactive_user_follow_user"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserFollowServiceProvider(AbstractFollowBase):
    class Meta:
        db_table = "interactive_user_follow_service_provider"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserFollowOthers(AbstractFollowBase):
    class Meta:
        db_table = "interactive_user_follow_others"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderFollowUser(AbstractFollowBase):
    class Meta:
        db_table = "interactive_sp_follow_user"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderFollowServiceProvider(AbstractFollowBase):
    class Meta:
        db_table = "interactive_sp_follow_sp"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderFollowOthers(AbstractFollowBase):
    class Meta:
        db_table = "interactive_sp_follow_others"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]