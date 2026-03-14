from typing import Any, Dict, List, Optional
from django.core.exceptions import ObjectDoesNotExist


def get_direct_data(obj: Any, fields: List[str]) -> Dict[str, Any]:
    return {field: getattr(obj, field) for field in fields}


def get_one_to_one_data(obj: Any, attr: str, fields: List[str],
                        extra_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    try:
        related_obj = getattr(obj, attr)
        data = {field: getattr(related_obj, field) for field in fields}
        if extra_fields:
            data.update(extra_fields)
        return data
    except ObjectDoesNotExist:
        return extra_fields or {}


def get_many_to_one_data(obj: Any, attr: str, fields: List[str]) -> List[Dict[str, Any]]:
    related_manager = getattr(obj, attr, None)
    if related_manager is None:
        return []
    return [
        {field: getattr(item, field, None) for field in fields}
        for item in related_manager.all()
    ]


def get_related_list_data(queryset: Any, fields: List[str]) -> List[Dict[str, Any]]:
    return [
        {field: getattr(item, field) for field in fields}
        for item in queryset
    ]


def get_new_code(model_name) -> int:
    last_code = model_name.objects.all().order_by('-code').first()

    if last_code:
        code = last_code.code + 1
    else:
        code = 1

    return code
