from rest_framework import exceptions
from rest_framework.exceptions import NotAcceptable
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.exceptions import APIException
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import UnsupportedMediaType
from rest_framework.exceptions import Throttled
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError


class BadRequest(APIException):
    status_code: int = 400
    default_detail: str = "Bad Request"
    default_code: str = "400"


class AccessDenied(APIException):
    status_code: int = 403
    default_detail: str = "Access Denied"
    default_code: str = "403"


class FailedDependency(APIException):
    status_code: int = 424
    default_detail: str = "Failed Request"
    default_code: str = "424"


class RetryAfter(APIException):
    status_code: int = 429
    default_detail: str = "Retry After"
    default_code: str = "429"


class IntegrityError(IntegrityError, APIException):
    status_code = 400
    default_detail = "Integrity error"


class DoesNotExist(APIException):
    default_detail = "Doesn't exists"
    status_code = 404
