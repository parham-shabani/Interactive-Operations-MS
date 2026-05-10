from rest_framework import serializers


class ScoreSerializer(serializers.Serializer):
    ACTOR_TYPE = [
        ("user", "User"),
        ("university", "University"),
        ("industry", "Industry"),
        ("business", "Business"),
    ]
    TARGET_TYPE = [
        # ("user", "User"),  not in score
        ("university", "University"),
        ("industry", "Industry"),
        ("business", "Business"),
        ("product", "Product"),
        ("service", "Service"),
        # ("comment", "Comment"),
    ]
    TARGET_TYPE_ENUM_SCORE_PARAM = [choice[0] for choice in TARGET_TYPE]

    actor_type = serializers.ChoiceField(choices=ACTOR_TYPE ,default='user')
    actor_id = serializers.IntegerField(default=0)
    target_type = serializers.ChoiceField(choices=TARGET_TYPE ,default='business')
    target_id = serializers.IntegerField(default=0)
    score = serializers.IntegerField(default=5)

    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("امتیاز باید عدد صحیح بین ۱ تا ۵ باشد.")
        return value
    
class ScoreAverageSerializer(serializers.Serializer):
    TARGET_TYPE = [
    # ("user", "User"),   not in score
    ("university", "University"),
    ("industry", "Industry"),
    ("business", "Business"),
    ("product", "Product"),
    ("service", "Service"),
    # ("comment", "Comment"),
]
    target_type = serializers.ChoiceField(choices=TARGET_TYPE ,default='business')
    target_id = serializers.IntegerField()
    average = serializers.FloatField(allow_null=True)
    count = serializers.IntegerField()