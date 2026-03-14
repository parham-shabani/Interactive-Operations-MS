from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Score(models.Model):
    ACTOR_TYPE = [
        ('user', 'User'),
        ('business', 'Business'),
        ('university', 'University'),
        ('industry', 'Industry'),
    ]
    TARGET_TYPE = [
        # ('user', 'User'), not in score
        ('university', 'University'),
        ('industry', 'Industry'),
        ('business', 'Business'),
        
        ('product', 'Product'),
        ('service', 'Service'),
        # ('comment', 'Comment'),
    ]

    TARGET_TYPE_ENUM_SCORE_PARAM = [choice[0] for choice in TARGET_TYPE]
    
    actor_type = models.CharField(max_length=50,choices=ACTOR_TYPE)
    actor_id = models.CharField(max_length=100)
    target_type = models.CharField(max_length=50,choices=TARGET_TYPE)
    target_id = models.CharField(max_length=100)
    
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [['actor_type', 'actor_id', 'target_type', 'target_id']]

        
        db_table = "interactive_score"
        indexes = [
            models.Index(fields=["target_type", "target_id"]),
        ]

    def __str__(self):
        return f"{self.target_type}:{self.target_id} -> {self.score}"