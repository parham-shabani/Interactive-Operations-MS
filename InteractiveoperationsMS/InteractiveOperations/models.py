
#models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import InteractiveOperations.enums as enums

class AbstractFollowBase(models.Model):
    actor_type = models.PositiveSmallIntegerField(choices=enums.ActorTypeBase)
    actor_id = models.PositiveBigIntegerField()
    target_type = models.PositiveSmallIntegerField(choices=enums.TargetTypeBase)
    target_id = models.PositiveBigIntegerField()
    is_active = models.BooleanField(default=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "actor_type",
                    "actor_id",
                    "target_type",
                    "target_id",
                ],
                name="uniq_follow_actor_target"
            )
        ]

class AbstractLikeBase(models.Model):
    actor_type = models.PositiveSmallIntegerField(choices=enums.ActorTypeBase)
    actor_id = models.PositiveBigIntegerField()
    target_type = models.PositiveSmallIntegerField(choices=enums.TargetTypeLike)
    target_id = models.PositiveBigIntegerField()
    like_status = models.PositiveSmallIntegerField(
        choices=enums.LikeStatusEnum.choices,
        default=enums.LikeStatusEnum.LIKE,
    )
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "actor_type",
                    "actor_id",
                    "target_type",
                    "target_id",
                ],
                name="uniq_like_actor_target"
            )
        ]


class AbstractScoreBase(models.Model):
    actor_type = models.PositiveSmallIntegerField(choices=enums.ActorTypeBase)
    actor_id = models.PositiveBigIntegerField()
    target_type = models.PositiveSmallIntegerField(choices=enums.TargetTypeScore)
    target_id = models.PositiveBigIntegerField()
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "actor_type",
                    "actor_id",
                    "target_type",
                    "target_id",
                ],
                name="uniq_score_actor_target"
            )
        ]

class AbstractShareBase(models.Model):

    actor_type = models.PositiveSmallIntegerField(choices=enums.ActorTypeBase)
    actor_id = models.PositiveBigIntegerField()
    target_type = models.PositiveSmallIntegerField(choices=enums.TargetTypeBase)
    target_id = models.PositiveBigIntegerField()
    platform = models.PositiveSmallIntegerField(
        choices=enums.SharePlatformEnum.choices,
        default=enums.SharePlatformEnum.IN_SITE
    )
    destination_type = models.CharField(max_length=50, null=True, blank=True)
    destination_id = models.PositiveSmallIntegerField(choices=enums.ActorTypeBase, null=True, blank=True)
    url = models.URLField(blank=True, default='')     #tavasote app url page gharar migirad
    reason = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

#follow
class UserFollowUser(AbstractFollowBase):
    class Meta:
        db_table = "interactive_user_follow_user"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserFollowServiceProvider(AbstractFollowBase):
    class Meta:
        db_table = "interactive_user_follow_service_provider"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserFollowOthers(AbstractFollowBase):
    class Meta:
        db_table = "interactive_user_follow_others"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderFollowUser(AbstractFollowBase):
    class Meta:
        db_table = "interactive_sp_follow_user"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderFollowServiceProvider(AbstractFollowBase):
    class Meta:
        db_table = "interactive_sp_follow_sp"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderFollowOthers(AbstractFollowBase):
    class Meta:
        db_table = "interactive_sp_follow_others"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

#like
class UserLikeUser(AbstractLikeBase):
    class Meta:
        db_table = "interactive_user_like_user"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserLikeServiceProvider(AbstractLikeBase):
    class Meta:
        db_table = "interactive_user_like_service_provider"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserLikeOthers(AbstractLikeBase):
    class Meta:
        db_table = "interactive_user_like_others"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderLikeUser(AbstractLikeBase):
    class Meta:
        db_table = "interactive_sp_like_user"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderLikeServiceProvider(AbstractLikeBase):
    class Meta:
        db_table = "interactive_sp_like_sp"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderLikeOthers(AbstractLikeBase):
    class Meta:
        db_table = "interactive_sp_like_others"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]


#share
class UserShareUser(AbstractShareBase):
    class Meta:
        db_table = "interactive_user_share_user"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserShareServiceProvider(AbstractShareBase):
    class Meta:
        db_table = "interactive_user_share_service_provider"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserShareOthers(AbstractShareBase):
    class Meta:
        db_table = "interactive_user_share_others"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderShareUser(AbstractShareBase):
    class Meta:
        db_table = "interactive_sp_share_user"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderShareServiceProvider(AbstractShareBase):
    class Meta:
        db_table = "interactive_sp_share_sp"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderShareOthers(AbstractShareBase):
    class Meta:
        db_table = "interactive_sp_share_others"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]        


#score
# class UserScoreUser(AbstractScoreBase):
#     class Meta:
#         db_table = "interactive_user_score_user"
#         indexes = [
#             models.Index(fields=["actor_id"]),
#             models.Index(fields=["target_id"]),
#         ]

class UserScoreServiceProvider(AbstractScoreBase):
    class Meta:
        db_table = "interactive_user_score_service_provider"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class UserScoreOthers(AbstractScoreBase):
    class Meta:
        db_table = "interactive_user_score_others"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

# class ServiceProviderScoreUser(AbstractScoreBase):
#     class Meta:
#         db_table = "interactive_sp_score_user"
#         indexes = [
#             models.Index(fields=["actor_id"]),
#             models.Index(fields=["target_id"]),
#         ]

class ServiceProviderScoreServiceProvider(AbstractScoreBase):
    class Meta:
        db_table = "interactive_sp_score_sp"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]

class ServiceProviderScoreOthers(AbstractScoreBase):
    class Meta:
        db_table = "interactive_sp_score_others"
        indexes = [
            models.Index(fields=["actor_id"]),
            models.Index(fields=["target_id"]),
        ]


#relations
class InteractiveRelations:

    @staticmethod
    def _normalize_actor_group(actor_type) -> str:
        """پشتیبانی از هر دو حالت عددی یا رشته‌ای برای actor_type."""
        # اگر عدد است، به رشته تبدیل کن
        if isinstance(actor_type, int):
            # مپ از Enum به رشته
            actor_map = {
                1: "user",
                2: "university",
                3: "industry",
                4: "business",
            }
            actor_type = actor_map.get(actor_type)

        if actor_type is None:
            raise ValueError(f"Unsupported actor_type: {actor_type}")

        actor_type = str(actor_type).lower()

        if actor_type == "user":
            return "user"
        if actor_type in ("business", "university", "industry"):
            return "service_provider"
        raise ValueError(f"Unsupported actor_type: {actor_type}")

    @staticmethod
    def _normalize_target_group(target_type) -> str:
        """پشتیبانی از هر دو حالت عددی یا رشته‌ای برای target_type."""
        if isinstance(target_type, int):
            target_map = {
                1: "user",
                2: "university",
                3: "industry",
                4: "business",
                5: "service",
                6: "product",
                7: "comment",
            }
            target_type = target_map.get(target_type)

        if target_type is None:
            raise ValueError(f"Unsupported target_type: {target_type}")

        target_type = str(target_type).lower()

        if target_type == "user":
            return "user"
        if target_type in ("business", "university", "industry"):
            return "service_provider"
        if target_type in ("service", "product", "comment"):
            return "others"
        raise ValueError(f"Unsupported target_type: {target_type}")


    FOLLOW_MODEL_MAP = {
        ("user", "user"): UserFollowUser,
        ("user", "service_provider"): UserFollowServiceProvider,
        ("user", "others"): UserFollowOthers,
        ("service_provider", "user"): ServiceProviderFollowUser,
        ("service_provider", "service_provider"): ServiceProviderFollowServiceProvider,
        ("service_provider", "others"): ServiceProviderFollowOthers,
    }
    LIKE_MODEL_MAP = {
        ("user", "user"): UserLikeUser,
        ("user", "service_provider"): UserLikeServiceProvider,
        ("user", "others"): UserLikeOthers,
        ("service_provider", "user"): ServiceProviderLikeUser,
        ("service_provider", "service_provider"): ServiceProviderLikeServiceProvider,
        ("service_provider", "others"): ServiceProviderLikeOthers,
    }
    SCORE_MODEL_MAP = {
        # ("user", "user"): iomodels.UserScoreUser,
        ("user", "service_provider"): UserScoreServiceProvider,
        ("user", "others"): UserScoreOthers,
        # ("service_provider", "user"): iomodels.ServiceProviderScoreUser,
        ("service_provider", "service_provider"): ServiceProviderScoreServiceProvider,
        ("service_provider", "others"): ServiceProviderScoreOthers,
    }
    SCORE_AVERAGE_MAP = {
        "service_provider": [
            UserScoreServiceProvider,
            ServiceProviderScoreServiceProvider,
        ],
        "others": [
            UserScoreOthers,
            ServiceProviderScoreOthers,
        ],
    }
    SHARE_MODEL_MAP = {
        ("user", "user"): UserShareUser,
        ("user", "service_provider"): UserShareServiceProvider,
        ("user", "others"): UserShareOthers,
        ("service_provider", "user"): ServiceProviderShareUser,
        ("service_provider", "service_provider"): ServiceProviderShareServiceProvider,
        ("service_provider", "others"): ServiceProviderShareOthers,
    }

    FOLLOWER_LIST_MAP = {
        "user": [
            UserFollowUser,
            ServiceProviderFollowUser,
        ],
        "service_provider": [
            UserFollowServiceProvider,
            ServiceProviderFollowServiceProvider,
        ],
        "others": [
            UserFollowOthers,
            ServiceProviderFollowOthers,
        ],
    }
    FOLLOWING_LIST_MAP = {
        "user": [
            UserFollowUser,
            UserFollowServiceProvider,
            UserFollowOthers,
        ],
        "service_provider": [
            ServiceProviderFollowUser,
            ServiceProviderFollowServiceProvider,
            ServiceProviderFollowOthers,
        ],
    }
    LIKER_LIST_MAP = {
        "user": [
            UserLikeUser,
            ServiceProviderLikeUser,
        ],
        "service_provider": [
            UserLikeServiceProvider,
            ServiceProviderLikeServiceProvider,
        ],
        "others": [
            UserLikeOthers,
            ServiceProviderLikeOthers,
        ],
    }
    LIKEE_LIST_MAP = {
        "user": [
            UserLikeUser,
            UserLikeServiceProvider,
            UserLikeOthers,
        ],
        "service_provider": [
            ServiceProviderLikeUser,
            ServiceProviderLikeServiceProvider,
            ServiceProviderLikeOthers,
        ],
    }
        