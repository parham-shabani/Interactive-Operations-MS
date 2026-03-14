# inoMS/InteractiveOperations/serializers.py
from rest_framework import serializers
from core.serializers import BaseResponseSerializer
import logging

logger = logging.getLogger(__name__)


class DataNameResponseSerializer(serializers.Serializer):
    actor_id = serializers.IntegerField()
    actor_type = serializers.CharField()
    actor_ids = serializers.ListField()


class NameResponseSerializer(BaseResponseSerializer):
    data = DataNameResponseSerializer()


class BadResponseSerializer(BaseResponseSerializer):
    data = DataNameResponseSerializer()