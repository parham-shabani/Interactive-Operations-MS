from rest_framework import serializers
from InteractiveOperations.models import Share, SharePlatform

class ShareSerializer(serializers.Serializer):
    ACTOR_TYPE = [
        ('user', 'User'),

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

        ('comment', 'Comment'),   
    ]


    actor_type = serializers.ChoiceField(choices=ACTOR_TYPE ,default='user')
    actor_id = serializers.IntegerField(default=0)
    target_type = serializers.ChoiceField(choices=TARGET_TYPE ,default='business')
    target_id = serializers.IntegerField(default=0)
    platform = serializers.ChoiceField(
        choices=[
            (SharePlatform.IN_SITE, 'In Site'),
            (SharePlatform.TELEGRAM, 'Telegram'),
            (SharePlatform.WHATSAPP, 'WhatsApp'),
        ],
        default=SharePlatform.IN_SITE
    )
    destination_type = serializers.ChoiceField(choices=TARGET_TYPE ,default='user')
    destination_id = serializers.IntegerField(default=0, allow_null=True)
    reason = serializers.CharField(default='', allow_blank=True)
    url = serializers.URLField(default='', allow_blank=True)
    
    
    class Meta:
        model = Share
        fields = [
            'id',
            'actor_type',
            'actor_id',
            'target_type',
            'target_id',
            'platform',
            'destination_type',
            'destination_id',
            'reason',
            'url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        platform = attrs.get('platform')
        destination_type = attrs.get('destination_type')
        destination_id = attrs.get('destination_id')

        if platform == SharePlatform.IN_SITE:
            if not destination_type or not destination_id:
                raise serializers.ValidationError("برای اشتراک در سایت، مقصد باید مشخص شود.")
        else:
            # در حالت تلگرام یا واتساپ نباید مقصد مشخص شود
            if destination_type or destination_id:
                raise serializers.ValidationError("در حالت اپ‌های خارجی مقصد نباید مشخص شود.")
        return attrs
