from typing import Any, Dict, List, Optional
from rest_framework import status
from rest_framework.renderers import JSONRenderer as BaseJSONRenderer
from rest_framework.response import Response as BaseResponse
import logging

logger = logging.getLogger(__name__)


class CustomRenderer(BaseJSONRenderer):
    def error_gets(self, errors, validation_errors, general_errors, data) -> None:
        for error_key, error_value in errors.items():
            if data["message"] == "ValidationError":
                validation_errors[error_key] = error_value
            else:
                general_errors[error_key] = error_value

    def generate_dict(self, data):
        if isinstance(data, dict) and data.get("status_code", None) is not None:
            data["success"] = True
        else:
            return {"data": data, "message": None, "status_code": 200, "success": True}

    def seprate_data(self, data: Dict) -> Dict:
        data["errors"] = {}
        data["success"] = True
        data["status_code"] = int(data.get("status_code", "200"))
        validation_errors: Dict = {}
        general_errors: Dict = {}
        if not (200 <= data["status_code"] and data["status_code"] < 300):
            data["success"] = False

        if not data["success"]:
            errors: Dict | List | None = data.get("data", None)
            if errors is not None:
                if isinstance(errors, dict):
                    self.error_gets(errors, validation_errors, general_errors, data)
                elif isinstance(errors, list):
                    for item in errors:
                        self.error_gets(item, validation_errors, general_errors, data)

                if validation_errors:
                    data["errors"] = validation_errors
                if general_errors:
                    logging.info(general_errors)

                data.update(
                    data=None,
                )

        return data

    def render(
            self, data: Dict, accepted_media_type=None, renderer_context=None
    ) -> bytes:
        return super().render(
            self.seprate_data(data),
            accepted_media_type,
            renderer_context,
        )


class Response(BaseResponse):
    def __init__(
            self,
            data: Optional[Dict] | Optional[List] | Optional[Any] = None,
            status: int = status.HTTP_200_OK,
            message: Optional[str] | Optional[Dict] | Optional[List] = None,
            headers=None,
            exception=False,
            exception_raise: Exception | None = None,
            content_type=None,
    ) -> None:
        logger.info("responses:__init__")
        response_dict: Dict = {
            "data": data,
            "message": message,
            "status_code": status,
        }
        super().__init__(
            data=response_dict,
            status=status,
            headers=headers,
            exception=exception,
            content_type=content_type,
            template_name=None,
        )
        self.exception_raise: Exception | None = exception_raise
