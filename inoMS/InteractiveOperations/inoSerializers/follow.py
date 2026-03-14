# InteractiveOperations/serializers/follow.py
from rest_framework import serializers
from InteractiveOperations.models import Follow
# from InteractiveOperations.models.follow  import Follow.ACTOR_TYPE, TARGET_TYPE



class FollowSerializer(serializers.Serializer):
    ACTOR_TYPE = [
        ('user', 'User'),
        #organiser?
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

        # ('individual', 'Individual'),

        ('product', 'Product'),
        ('service', 'Service'),
        
        # ('comment', 'Comment'),
    ]

    class Meta:
        model = Follow
        fields = ["actor_type", "actor_id", "target_type", "target_id", "is_active", "created_at", "updated_at"]
        read_only_fields = ['id', 'created_at', 'updated_at']

    actor_type = serializers.ChoiceField(choices=ACTOR_TYPE ,default='user')
    actor_id = serializers.IntegerField(default=0)
    target_type = serializers.ChoiceField(choices=TARGET_TYPE ,default='user')
    target_id = serializers.IntegerField(default=0)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class FollowerItemSerializer(serializers.Serializer):
    actor_type = serializers.CharField()
    actor_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class FollowingItemSerializer(serializers.Serializer):
    target_type = serializers.CharField()
    target_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class FollowersListSerializer(serializers.Serializer):
    target_type = serializers.CharField()
    target_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = FollowerItemSerializer(many=True)

class FollowingsListSerializer(serializers.Serializer):
    actor_type = serializers.CharField()
    actor_id = serializers.IntegerField()
    count = serializers.IntegerField()
    results = FollowingItemSerializer(many=True)