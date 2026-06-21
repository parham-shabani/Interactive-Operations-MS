from typing import Any, Callable, Dict, NoReturn, Optional, Type
from .exceptions import NotAcceptable
from .exceptions import NotAuthenticated
from .exceptions import NotFound
from .exceptions import MethodNotAllowed
from .exceptions import APIException
from .exceptions import AuthenticationFailed
from .exceptions import ParseError
from .exceptions import PermissionDenied
from .exceptions import UnsupportedMediaType
from .exceptions import Throttled
from .exceptions import ValidationError
from .exceptions import IntegrityError
from .exceptions import DoesNotExist
from .exceptions import RetryAfter
from .exceptions import BadRequest, AccessDenied, FailedDependency
from django.http import Http404
from blinker import Signal
import logging
from django.utils.translation import gettext_lazy as _
from .responses import Response


class HTTPException(APIException):
    code: int
    detail: str


def raise_500_error(
        sender: HTTPException | Exception | APIException, **kwargs
) -> NoReturn:  # type: ignore
    global logger
    logger.error(f"{type(sender).__name__}:{sender}")


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s | %(funcName)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S:%MS",
)
for logger_name in ["boto", "boto3", "botocore", "botocore.loaders", "botocore.hooks"]:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)
logger: logging.Logger = logging.getLogger("exceptions")
signal: Signal = Signal("Handler")
signal.connect(raise_500_error)


class Http500Response(Response):
    status_code: int = 500

    def close(self) -> None:
        super().close()
        global signal

        signal.send(self.exception_raise)
        raise self.exception_raise


class HTTPExceptionHandler:
    def __init__(
            self,
            exceptions: Dict[
                Type[HTTPException], Callable[[HTTPException, Any], Response]
            ] = dict(),
    ) -> None:
        self.exceptions: Dict[
            Type[HTTPException], Callable[[HTTPException, Any], Response]
        ] = exceptions

    def add_exception_handler(
            self,
            exception: Type[HTTPException] | Any,
            handler: Callable[[HTTPException, Any], Response] | None = None,
    ) -> None:
        if handler:
            self.exceptions[exception] = handler
        else:
            self.exceptions[exception] = self.base_exception_handler

    def base_exception_handler(self, exc: HTTPException, context: Any) -> Response:
        try:
            message: str = exc.detail
        except:
            message = exc.default_detail

        try:
            if isinstance(exc.detail.code, int) or (
                    isinstance(exc.detail.code, str) and exc.detail.code.isdigit()
            ):
                status_code = exc.detail.code
            else:
                status_code: int = exc.code
        except:
            status_code = exc.status_code

        return Response(
            data=None,
            message=message,
            status=status_code,
        )

    def unhanled_exception_handler(self, unknown_exc: Exception) -> Response:
        exc: HTTPException = HTTPException()
        return Http500Response(
            message=_("Internal server error"),
            status=exc.status_code,
            data=None,
            exception_raise=unknown_exc,
        )

    def handle(self, exc: HTTPException, context: Any) -> Response:
        if type(exc) in self.exceptions:
            handler: Callable[[HTTPException, Any], Response] = self.exceptions[
                type(exc)
            ]
            return handler(exc, context)
        return self.unhanled_exception_handler(exc)


handler: HTTPExceptionHandler = HTTPExceptionHandler()


def validation_exception_handler(
        exc: ValidationError | HTTPException, context: Any
) -> Response:
    try:
        message: str = exc.detail  # type: ignore
    except:
        message: str = exc.default_detail

    try:
        status_code: int = exc.code  # type: ignore
    except:
        status_code: int = exc.status_code

    return Response(
        data=message,
        message=exc.__class__.__name__,
        status=status_code,
    )


def http_exception_handler(exc: Http404, context: Any) -> Response:
    exception = NotFound
    return Response(
        data=None,
        message=exception.default_detail,
        status=exception.status_code,
    )


handler.add_exception_handler(NotAcceptable)
handler.add_exception_handler(NotAuthenticated)
handler.add_exception_handler(NotFound)
handler.add_exception_handler(MethodNotAllowed)
handler.add_exception_handler(APIException)
handler.add_exception_handler(AuthenticationFailed)
handler.add_exception_handler(ParseError)
handler.add_exception_handler(PermissionDenied)
handler.add_exception_handler(UnsupportedMediaType)
handler.add_exception_handler(BadRequest)
handler.add_exception_handler(AccessDenied)
handler.add_exception_handler(FailedDependency)
handler.add_exception_handler(Throttled)
handler.add_exception_handler(RetryAfter)
handler.add_exception_handler(Http404, http_exception_handler)
handler.add_exception_handler(DoesNotExist, http_exception_handler)
handler.add_exception_handler(ValidationError, validation_exception_handler)

api_exception_handler: Callable[[HTTPException, Any], Response] = handler.handle
