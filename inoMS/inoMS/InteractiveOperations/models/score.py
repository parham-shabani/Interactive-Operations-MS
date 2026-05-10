# InteractiveOperations/models/score.py
from django.db import models
from .base_score import AbstractScoreBase

# class UserScoreUser(AbstractScoreBase):
#     class Meta:
#         db_table = "interactive_user_score_user"
#         unique_together = ("actor_id", "target_id")
#         indexes = [
#             models.Index(fields=["actor_id"]),
#             models.Index(fields=["target_id"]),
#         ]

class UserScoreServiceProvider(AbstractScoreBase):
    class Meta:
        db_table = "interactive_user_score_service_provider"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserScoreOthers(AbstractScoreBase):
    class Meta:
        db_table = "interactive_user_score_others"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

# class ServiceProviderScoreUser(AbstractScoreBase):
#     class Meta:
#         db_table = "interactive_sp_score_user"
#         unique_together = ("actor_id", "target_id")
#         indexes = [
#             models.Index(fields=["actor_id"]),
#             models.Index(fields=["target_id"]),
#         ]

class ServiceProviderScoreServiceProvider(AbstractScoreBase):
    class Meta:
        db_table = "interactive_sp_score_sp"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderScoreOthers(AbstractScoreBase):
    class Meta:
        db_table = "interactive_sp_score_others"
        unique_together = ("actor_id", "target_id")
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]