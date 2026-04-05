# InteractiveOperations/serializers/follow.py
from rest_framework import serializers


class FollowSerializer(serializers.Serializer):
    ACTOR_TYPE = [
        ("user", "User"),
        ("university", "University"),
        ("industry", "Industry"),
        ("business", "Business"),
    ]
    TARGET_TYPE = [
        ("user", "User"),
        ("university", "University"),
        ("industry", "Industry"),
        ("business", "Business"),
        ("product", "Product"),
        ("service", "Service"),    
        # ("comment", "Comment"),
    ]

    ACTOR_TYPE_ENUM_FOLLOW_PARAM = [choice[0] for choice in ACTOR_TYPE]
    TARGET_TYPE_ENUM_FOLLOW_PARAM = [choice[0] for choice in TARGET_TYPE]

    actor_type = serializers.ChoiceField(choices=ACTOR_TYPE, default="user")
    actor_id = serializers.IntegerField(default=0)
    target_type = serializers.ChoiceField(choices=TARGET_TYPE, default="user")
    target_id = serializers.IntegerField(default=0)
    is_active = serializers.BooleanField(default=True)

class FollowerItemSerializer(serializers.Serializer):
    actor_type = serializers.CharField()
    actor_id = serializers.IntegerField()
    last_updated_at = serializers.DateTimeField()

class FollowersListSerializer(serializers.Serializer):
    target_type = serializers.CharField()
    target_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = FollowerItemSerializer(many=True)

class FollowingItemSerializer(serializers.Serializer):
    target_type = serializers.CharField()
    target_id = serializers.IntegerField()
    last_updated_at = serializers.DateTimeField()

class FollowingsListSerializer(serializers.Serializer):
    actor_type = serializers.CharField()
    actor_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = FollowingItemSerializer(many=True)
