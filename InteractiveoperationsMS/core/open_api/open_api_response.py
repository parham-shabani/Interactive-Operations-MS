from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from core import serializers as core_serializers
from core.open_api import swagger_example_values as core_swagger_example_values

responses_400 = OpenApiResponse(
    response=core_serializers.BaseResponseSerializer,
    description="Bad request example",
    examples=[
        OpenApiExample(
            "Bad request example",
            value=core_swagger_example_values.bad_request_error,
        )
    ],
)

responses_401 = OpenApiResponse(
    response=core_serializers.BaseResponseSerializer,
    description="Unauthorized response body",
    examples=[
        OpenApiExample(
            "Unauthorized Example",
            value=core_swagger_example_values.unauthorized_error,
        )
    ],
)

responses_403 = OpenApiResponse(
    response=core_serializers.BaseResponseSerializer,
    description="Forbidden access response body",
    examples=[
        OpenApiExample(
            "Forbidden Access Example",
            value=core_swagger_example_values.forbidden_access_error,
        )
    ],
)

responses_404 = OpenApiResponse(
    response=core_serializers.BaseResponseSerializer,
    description="Not found response body",
    examples=[
        OpenApiExample(
            "Not found. Example",
            value=core_swagger_example_values.not_found_error,
        )
    ],
)

responses_429 = OpenApiResponse(
    response=core_serializers.BaseResponseSerializer,
    description="Too many requests",
    examples=[
        OpenApiExample(
            "Too Many Requests Example",
            value=core_swagger_example_values.too_many_requests_error,
        )
    ],
)

responses_500 = OpenApiResponse(
    response=core_serializers.BaseResponseSerializer,
    description="Internal server error response body",
    examples=[
        OpenApiExample(
            "Internal Server Error Example",
            value=core_swagger_example_values.internal_server_error,
        )
    ],
)
