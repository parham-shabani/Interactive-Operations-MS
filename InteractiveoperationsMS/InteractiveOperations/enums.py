
#enums.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class LikeStatusEnum(models.IntegerChoices):
    LIKE = 1, _("like")
    NONE = 2, _("none")
    DISLIKE = 3, _("dislike")


class SharePlatformEnum(models.IntegerChoices):
    IN_SITE = 1, _("in site")
    TELEGRAM = 2, _("telegram")
    WHATSAPP = 3, _("whatsapp")


class ActorTypeBase(models.IntegerChoices):
    USER = 1, _("user")
    UNIVERSITY = 2, _("university")
    INDUSTRY = 3, _("industry")
    BUSINESS = 4, _("business")


class TargetTypeLike(models.IntegerChoices):
    USER = 1, _("user")
    UNIVERSITY = 2, _("university")
    INDUSTRY = 3, _("industry")
    BUSINESS = 4, _("business")
    PRODUCT = 5, _("product")
    SERVICE = 6, _("service")
    COMMENT = 7, _("comment")

class TargetTypeBase(models.IntegerChoices):
    USER = 1, _("user")
    UNIVERSITY = 2, _("university")
    INDUSTRY = 3, _("industry")
    BUSINESS = 4, _("business")
    PRODUCT = 5, _("product")
    SERVICE = 6, _("service")

class TargetTypeScore(models.IntegerChoices):
    # USER = 1, _("user")
    UNIVERSITY = 2, _("university")
    INDUSTRY = 3, _("industry")
    BUSINESS = 4, _("business")
    PRODUCT = 5, _("product")
    SERVICE = 6, _("service")


TYPE_INT_TO_STR = {
    TargetTypeLike.USER.value: "user",
    TargetTypeLike.UNIVERSITY.value: "university",
    TargetTypeLike.INDUSTRY.value: "industry",
    TargetTypeLike.BUSINESS.value: "business",
    TargetTypeLike.SERVICE.value: "service",
    TargetTypeLike.PRODUCT.value: "product",
    TargetTypeLike.COMMENT.value: "comment",

}

TARGET_TYPE_INT_TO_STR = TYPE_INT_TO_STR
ACTOR_TYPE_INT_TO_STR = TYPE_INT_TO_STR