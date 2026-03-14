from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DynamicFieldsSerializer(serializers.Serializer):
    """
    A Serializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CustomChoiceField(serializers.ChoiceField):
    """
    choices:[(1, 'User'), (2, 'Admin'), .....]
    self.choice_dict:{1: 'User', 2: 'Admin', .... }
    self.reverse_dict:{'User': 1, 'Admin': 2, ....}
    """

    def __init__(self, choices=None, **kwargs):

        if choices:
            self.choice_dict = dict(choices)
            self.reverse_dict = {v: k for k, v in self.choice_dict.items()}
        super().__init__(choices=[(v, v) for k, v in choices], **kwargs)

    def to_internal_value(self, data):
        if data not in self.reverse_dict:
            self.fail("invalid_choice", input=data)
        return self.reverse_dict[data]

    def to_representation(self, value):
        return self.choice_dict.get(value, value)


class BaseResponseSerializer(serializers.Serializer):
    data = serializers.SerializerMethodField(allow_null=True, required=False)
    message = serializers.CharField(allow_null=True, required=False)
    status_code = serializers.IntegerField()
    errors = serializers.DictField()
    success = serializers.BooleanField()

    @extend_schema_field(serializers.DictField(allow_null=True))
    def get_data(self, obj):
        """ Dynamic data value"""
        # return obj.get("data", {})
        return obj.get("data", None)


class GetIdsListSerializer(serializers.Serializer):
    ids = serializers.ListSerializer(child=serializers.IntegerField())


class GetIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class GetStringListSerializer(serializers.Serializer):
    str_list = serializers.ListSerializer(child=serializers.CharField())


class FileUploadSerializer(serializers.Serializer):
    """
    Note: use FILE_UPLOAD_HANDLERS in setting.py
    """
    file = serializers.FileField()
