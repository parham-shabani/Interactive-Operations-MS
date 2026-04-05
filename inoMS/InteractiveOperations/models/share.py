from django.db import models
from .base_share import AbstractShareBase

class UserShareUser(AbstractShareBase):
    class Meta:
        db_table = "interactive_user_share_user"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserShareServiceProvider(AbstractShareBase):
    class Meta:
        db_table = "interactive_user_share_service_provider"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserShareOthers(AbstractShareBase):
    class Meta:
        db_table = "interactive_user_share_others"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderShareUser(AbstractShareBase):
    class Meta:
        db_table = "interactive_sp_share_user"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderShareServiceProvider(AbstractShareBase):
    class Meta:
        db_table = "interactive_sp_share_sp"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderShareOthers(AbstractShareBase):
    class Meta:
        db_table = "interactive_sp_share_others"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]