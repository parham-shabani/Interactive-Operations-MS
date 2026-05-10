from django.db import models
from .base import InteractionBase
from django.core.validators import MinValueValidator, MaxValueValidator

class AbstractScoreBase(InteractionBase):
    actor_type = models.CharField(max_length=50)
    actor_id = models.CharField(max_length=100)
    target_type = models.CharField(max_length=50)
    target_id = models.CharField(max_length=100)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
