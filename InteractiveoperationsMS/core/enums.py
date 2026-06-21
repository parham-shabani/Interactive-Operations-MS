# inoMS/core/enums.py
from django.db import models
from django.utils.translation import gettext_lazy as _


Accept_Language_List = ['en', 'fa']

BOOLEAN_CHOICES = ((True, 'Yes'), (False, 'No'))

ACTOR_TYPE = [
    (1, "User"),
    (2, "Admin"),
    (3, "Organiser"),  # no need token and authentication
    (4, "University"),
    (5, "Industry"),
    (6, "Business"),
    (9, "Individual"),  # no need token and authentication
]



ACTOR_LABEL_TO_ID = {label: value for value, label in ACTOR_TYPE}
ACTOR_ID_TO_LABEL = {value: label for value, label in ACTOR_TYPE}


class ActorType(models.IntegerChoices):
    User = 1, _('User')
    Admin = 2, _('Admin')
    Organiser = 3, _('Organiser')  # no need token and authentication
    University = 4, _('University')
    Industry = 5, _('Industry')
    Business = 6, _('Business')
    Product = 7, _('Product')
    Comment = 8, _('Comment')
    Individual = 9, _('Individual')  # no need token and authentication
