from rest_framework import serializers

class ShareSerializer(serializers.Serializer):
    ACTOR_TYPE = [
        ('user', 'User'),
        ('university', 'University'),
        ('industry', 'Industry'),
        ('business', 'Business'),
    ]
    TARGET_TYPE = [
        ('user', 'User'),
        ('university', 'University'),
        ('industry', 'Industry'),
        ('business', 'Business'),
        ('product', 'Product'),
        ('service', 'Service'),
        ('comment', 'Comment'),   
    ]
    SHARE_PLATFORM_CHOICES = [
        ('in site', 'In Site'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
    ]

    actor_type = serializers.ChoiceField(choices=ACTOR_TYPE, default='user')
    actor_id = serializers.IntegerField(default=0)
    target_type = serializers.ChoiceField(choices=TARGET_TYPE, default='business')
    target_id = serializers.IntegerField(default=0)
    platform = serializers.ChoiceField(choices=SHARE_PLATFORM_CHOICES, default='in site')
    destination_type = serializers.ChoiceField(choices=TARGET_TYPE, required=False, allow_null=True, allow_blank=True)
    destination_id = serializers.IntegerField(required=False, allow_null=True)
    reason = serializers.CharField(required=False, default='', allow_blank=True)
    url = serializers.URLField(required=False, default='', allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)

    def to_internal_value(self, data):
        data = data.copy()

        if data.get("destination_type", None) == "":
            data["destination_type"] = None

        if data.get("destination_id", None) == "":
            data["destination_id"] = None

        if data.get("url", None) == "":
            data["url"] = ""

        if data.get("reason", None) == "":
            data["reason"] = ""

        return super().to_internal_value(data)

    
    def validate(self, attrs):
        platform = attrs.get('platform')
        destination_type = attrs.get('destination_type')
        destination_id = attrs.get('destination_id')

        if platform == 'in site':
            if not destination_type or not destination_id:
                raise serializers.ValidationError("برای اشتراک در سایت، مقصد باید مشخص شود.")
        else:
            # در حالت تلگرام یا واتساپ نباید مقصد مشخص شود
            if destination_type or destination_id:
                raise serializers.ValidationError("در حالت اپ‌های خارجی مقصد نباید مشخص شود.")
        return attrs
