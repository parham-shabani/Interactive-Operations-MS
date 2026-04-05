from InteractiveOperations import models as iomodels


class InteractiveRelations:
    def _normalize_actor_group(actor_type: str) -> str:
        if actor_type == "user":
            return "user"
        if actor_type in ("business", "university", "industry"):
            return "service_provider"
        raise ValueError(f"Unsupported actor_type: {actor_type}")

    def _normalize_target_group(target_type: str) -> str:
        if target_type == "user":
            return "user"
        if target_type in ("business", "university", "industry"):
            return "service_provider"
        if target_type in ("service", "product", "comment"):
            return "others"
        raise ValueError(f"Unsupported target_type: {target_type}")

    FOLLOW_MODEL_MAP = {
        ("user", "user"): iomodels.UserFollowUser,
        ("user", "service_provider"): iomodels.UserFollowServiceProvider,
        ("user", "others"): iomodels.UserFollowOthers,
        ("service_provider", "user"): iomodels.ServiceProviderFollowUser,
        ("service_provider", "service_provider"): iomodels.ServiceProviderFollowServiceProvider,
        ("service_provider", "others"): iomodels.ServiceProviderFollowOthers,
    }
    LIKE_MODEL_MAP = {
        ("user", "user"): iomodels.UserLikeUser,
        ("user", "service_provider"): iomodels.UserLikeServiceProvider,
        ("user", "others"): iomodels.UserLikeOthers,
        ("service_provider", "user"): iomodels.ServiceProviderLikeUser,
        ("service_provider", "service_provider"): iomodels.ServiceProviderLikeServiceProvider,
        ("service_provider", "others"): iomodels.ServiceProviderLikeOthers,
    }
    SCORE_MODEL_MAP = {
        # ("user", "user"): iomodels.UserScoreUser,
        ("user", "service_provider"): iomodels.UserScoreServiceProvider,
        ("user", "others"): iomodels.UserScoreOthers,
        # ("service_provider", "user"): iomodels.ServiceProviderScoreUser,
        ("service_provider", "service_provider"): iomodels.ServiceProviderScoreServiceProvider,
        ("service_provider", "others"): iomodels.ServiceProviderScoreOthers,
    }
    SCORE_AVERAGE_MAP = {
        "service_provider": [
            iomodels.UserScoreServiceProvider,
            iomodels.ServiceProviderScoreServiceProvider,
        ],
        "others": [
            iomodels.UserScoreOthers,
            iomodels.ServiceProviderScoreOthers,
        ],
    }
    SHARE_MODEL_MAP = {
        ("user", "user"): iomodels.UserShareUser,
        ("user", "service_provider"): iomodels.UserShareServiceProvider,
        ("user", "others"): iomodels.UserShareOthers,
        ("service_provider", "user"): iomodels.ServiceProviderShareUser,
        ("service_provider", "service_provider"): iomodels.ServiceProviderShareServiceProvider,
        ("service_provider", "others"): iomodels.ServiceProviderShareOthers,
    }

    FOLLOWER_LIST_MAP = {
        "user": [
            iomodels.UserFollowUser,
            iomodels.ServiceProviderFollowUser,
        ],
        "service_provider": [
            iomodels.UserFollowServiceProvider,
            iomodels.ServiceProviderFollowServiceProvider,
        ],
        "others": [
            iomodels.UserFollowOthers,
            iomodels.ServiceProviderFollowOthers,
        ],
    }
    FOLLOWING_LIST_MAP = {
        "user": [
            iomodels.UserFollowUser,
            iomodels.UserFollowServiceProvider,
            iomodels.UserFollowOthers,
        ],
        "service_provider": [
            iomodels.ServiceProviderFollowUser,
            iomodels.ServiceProviderFollowServiceProvider,
            iomodels.ServiceProviderFollowOthers,
        ],
    }
    LIKER_LIST_MAP = {
        "user": [
            iomodels.UserLikeUser,
            iomodels.ServiceProviderLikeUser,
        ],
        "service_provider": [
            iomodels.UserLikeServiceProvider,
            iomodels.ServiceProviderLikeServiceProvider,
        ],
        "others": [
            iomodels.UserLikeOthers,
            iomodels.ServiceProviderLikeOthers,
        ],
    }
    LIKEE_LIST_MAP = {
        "user": [
            iomodels.UserLikeUser,
            iomodels.UserLikeServiceProvider,
            iomodels.UserLikeOthers,
        ],
        "service_provider": [
            iomodels.ServiceProviderLikeUser,
            iomodels.ServiceProviderLikeServiceProvider,
            iomodels.ServiceProviderLikeOthers,
        ],
    }
