# inoMS/InteractiveOperations/serializers.py

from rest_framework import serializers
from core.serializers import BaseResponseSerializer
from . import enums as enums
import logging

logger = logging.getLogger(__name__)


class DataNameResponseSerializer(serializers.Serializer):
    actor_id = serializers.IntegerField()
    actor_type = serializers.IntegerField()
    actor_ids = serializers.ListField()


class NameResponseSerializer(BaseResponseSerializer):
    data = DataNameResponseSerializer()


class BadResponseSerializer(BaseResponseSerializer):
    data = DataNameResponseSerializer()


class FollowSerializer(serializers.Serializer):
    actor_type = serializers.ChoiceField(choices=enums.ActorTypeBase.choices,default=enums.ActorTypeBase.USER)
    actor_id = serializers.IntegerField(default=0)
    target_type = serializers.ChoiceField(choices=enums.TargetTypeBase.choices,default=enums.TargetTypeBase.USER)
    target_id = serializers.IntegerField(default=0)
    is_active = serializers.BooleanField(default=True)

    ACTOR_TYPE_ENUM_FOLLOW_PARAM = [choice[0] for choice in enums.ActorTypeBase.choices]
    TARGET_TYPE_ENUM_FOLLOW_PARAM = [choice[0] for choice in enums.TargetTypeBase.choices]


class FollowerItemSerializer(serializers.Serializer):
    actor_type = serializers.IntegerField()
    actor_id = serializers.IntegerField()
    last_updated_at = serializers.DateTimeField()

class FollowersListSerializer(serializers.Serializer):
    target_type = serializers.IntegerField()
    target_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = FollowerItemSerializer(many=True)

class FollowingItemSerializer(serializers.Serializer):
    target_type = serializers.IntegerField()
    target_id = serializers.IntegerField()
    last_updated_at = serializers.DateTimeField()

class FollowingsListSerializer(serializers.Serializer):
    actor_type = serializers.IntegerField()
    actor_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = FollowingItemSerializer(many=True)



class LikeSerializer(serializers.Serializer):
    actor_type = serializers.ChoiceField(choices=enums.ActorTypeBase.choices, default=enums.ActorTypeBase.USER)
    actor_id = serializers.IntegerField(default=0)
    target_type = serializers.ChoiceField(choices=enums.TargetTypeLike.choices,default=enums.TargetTypeLike.USER)
    target_id = serializers.IntegerField(default=0)
    like_status = serializers.ChoiceField(choices=enums.LikeStatusEnum.choices, default=enums.LikeStatusEnum.LIKE)

    ACTOR_TYPE_ENUM_LIKE_PARAM = [choice[0] for choice in enums.ActorTypeBase.choices]
    TARGET_TYPE_ENUM_LIKE_PARAM = [choice[0] for choice in enums.TargetTypeBase.choices]


class LikersItemSerializer(serializers.Serializer):
    actor_type = serializers.IntegerField()
    actor_id = serializers.IntegerField()
    last_updated_at = serializers.DateTimeField()


class LikeesItemSerializer(serializers.Serializer):
    target_type = serializers.IntegerField()
    target_id = serializers.IntegerField()
    last_updated_at = serializers.DateTimeField()


class LikersListSerializer(serializers.Serializer):
    target_type = serializers.IntegerField()
    target_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = LikersItemSerializer(many=True)


class LikeesListSerializer(serializers.Serializer):
    actor_type = serializers.IntegerField()
    actor_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = LikeesItemSerializer(many=True)


class DislikersItemSerializer(serializers.Serializer):
    actor_type = serializers.IntegerField()
    actor_id = serializers.IntegerField()
    last_updated_at = serializers.DateTimeField()


class DislikeesItemSerializer(serializers.Serializer):
    target_type = serializers.IntegerField()
    target_id = serializers.IntegerField()
    last_updated_at = serializers.DateTimeField()


class DislikersListSerializer(serializers.Serializer):
    target_type = serializers.IntegerField()
    target_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = DislikersItemSerializer(many=True)


class DislikeesListSerializer(serializers.Serializer):
    actor_type = serializers.IntegerField()
    actor_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = DislikeesItemSerializer(many=True)


class ShareSerializer(serializers.Serializer):
    actor_type = serializers.ChoiceField(
        choices=enums.ActorTypeBase.choices,
        default=enums.ActorTypeBase.USER
    )
    actor_id = serializers.IntegerField(default=0)

    target_type = serializers.ChoiceField(
        choices=enums.TargetTypeLike.choices,
        default=enums.TargetTypeLike.BUSINESS
    )
    target_id = serializers.IntegerField(default=0)

    platform = serializers.ChoiceField(
        choices=enums.SharePlatformEnum.choices,
        default=enums.SharePlatformEnum.IN_SITE
    )

    destination_type = serializers.ChoiceField(
        choices=enums.TargetTypeLike.choices,
        required=False,
        allow_null=True
    )

    destination_id = serializers.IntegerField(required=False, allow_null=True)
    reason = serializers.CharField(required=False, default='', allow_blank=True)
    url = serializers.URLField(required=False, default='', allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        platform = attrs.get('platform')
        destination_type = attrs.get('destination_type')
        destination_id = attrs.get('destination_id')

        if platform == enums.SharePlatformEnum.IN_SITE:
            if not destination_type or not destination_id:
                raise serializers.ValidationError(
                    "برای اشتراک در سایت، مقصد باید مشخص شود."
                )
        else:
            if destination_type or destination_id:
                raise serializers.ValidationError(
                    "در حالت اپ‌های خارجی مقصد نباید مشخص شود."
                )

        return attrs


class ScoreSerializer(serializers.Serializer):
    actor_type = serializers.ChoiceField(choices=enums.ActorTypeBase.choices,default=enums.ActorTypeBase.USER)
    actor_id = serializers.IntegerField(default=0)
    target_type = serializers.ChoiceField(choices=enums.TargetTypeScore.choices,default=enums.TargetTypeScore.BUSINESS)
    target_id = serializers.IntegerField(default=0)
    score = serializers.IntegerField(default=5)

    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "امتیاز باید عدد صحیح بین ۱ تا ۵ باشد."
            )
        return value


class ScoreAverageSerializer(serializers.Serializer):
    TARGET_TYPE_ENUM_SCORE_PARAM = [choice[0] for choice in enums.TargetTypeBase.choices]

    target_type = serializers.ChoiceField(
        choices=enums.TargetTypeBase.choices,
        default=enums.TargetTypeBase.BUSINESS
    )
    target_id = serializers.IntegerField()
    average = serializers.FloatField(allow_null=True)
    count = serializers.IntegerField()
