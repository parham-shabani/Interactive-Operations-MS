from rest_framework import serializers


class LikeSerializer(serializers.Serializer):
    LIKE = "like"
    DISLIKE = "dislike"
    NONE = "none"

    STATUS_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
        (NONE, "None"),
    ]

    ACTOR_TYPE = [
        ("user", "User"),
        ("university", "University"),
        ("industry", "Industry"),
        ("business", "Business"),
        # ("individual", "Individual"),
    ]

    TARGET_TYPE = [
        ("user", "User"),
        ("university", "University"),
        ("industry", "Industry"),
        ("business", "Business"),
        # ("individual", "Individual"),
        ("product", "Product"),
        ("service", "Service"),
        ("comment", "Comment"),
    ]

    actor_type = serializers.ChoiceField(choices=ACTOR_TYPE, default="user")
    actor_id = serializers.IntegerField(default=0)
    target_type = serializers.ChoiceField(choices=TARGET_TYPE, default="comment")
    target_id = serializers.IntegerField(default=0)
    like_status = serializers.ChoiceField(choices=STATUS_CHOICES, default="like")
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

"""
****************************************** like serializers *******************************************************************
"""
class LikersItemSerializer(serializers.Serializer):
    actor_type = serializers.CharField()
    actor_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class LikeesItemSerializer(serializers.Serializer):
    target_type = serializers.CharField()
    target_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class LikersListSerializer(serializers.Serializer):
    target_type = serializers.CharField()
    target_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = LikersItemSerializer(many=True)

class LikeesListSerializer(serializers.Serializer):
    actor_type = serializers.CharField()
    actor_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = LikeesItemSerializer(many=True)
"""
****************************************** Dislike serializers *******************************************************************
"""
class DislikersItemSerializer(serializers.Serializer):
    actor_type = serializers.CharField()
    actor_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class DislikeesItemSerializer(serializers.Serializer):
    target_type = serializers.CharField()
    target_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class DislikersListSerializer(serializers.Serializer):
    target_type = serializers.CharField()
    target_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = DislikersItemSerializer(many=True)

class DislikeesListSerializer(serializers.Serializer):
    actor_type = serializers.CharField()
    actor_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = DislikeesItemSerializer(many=True)