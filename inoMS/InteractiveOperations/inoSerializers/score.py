from rest_framework import serializers
from InteractiveOperations.models import Score


class ScoreSerializer(serializers.Serializer):

    ACTOR_TYPE = [
        ('user', 'User'),
        
        ('university', 'University'),
        ('industry', 'Industry'),
        ('business', 'Business'),

        # ('individual', 'Individual'),
    ]
    TARGET_TYPE = [
        # ('user', 'User'), not in score
        
        ('university', 'University'),
        ('industry', 'Industry'),
        ('business', 'Business'),

        # ('individual', 'Individual'),
        
        ('product', 'Product'),
        ('service', 'Service'),

        # ('comment', 'Comment'),
    ]

    actor_type = serializers.ChoiceField(choices=ACTOR_TYPE ,default='user')
    actor_id = serializers.IntegerField(default=0)
    target_type = serializers.ChoiceField(choices=TARGET_TYPE ,default='business')
    target_id = serializers.IntegerField(default=0)
    score = serializers.IntegerField(default=5)

    class Meta:
        model = Score
        fields = [
            'id',
            'actor_type',
            'actor_id',
            'target_type',
            'target_id',
            'score',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("امتیاز باید عدد صحیح بین ۱ تا ۵ باشد.")
        return value
    
class ScoreAverageSerializer(serializers.Serializer):
    target_type = serializers.ChoiceField(choices=[('university', 'University'),('industry', 'Industry'),
                                                   ('business', 'Business'),('product', 'Product'),('service', 'Service'),]
                                                   , default='business')
    target_id = serializers.IntegerField()
    average = serializers.FloatField(allow_null=True)
    count = serializers.IntegerField()