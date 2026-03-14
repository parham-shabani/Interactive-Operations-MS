from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from django.utils.decorators import method_decorator
from django.utils import translation
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.permissions import BasePermission
from core.responses import Response
from core.extensions.jwt.interfaces import TokenInterface
from core.extensions.jwt.tokens import BearerToken
from core.auth_tools.loaders import user_loader
from root import settings
import zoneinfo
import logging

logger = logging.getLogger(__name__)


class BaseMiddleware:
    def __init__(
            self,
            exclude_urls: List[str] = [],
            include_urls: List[str] = [],
    ) -> None:
        self.exclude_urls: List[str] = exclude_urls
        self.include_urls: List[str] = include_urls

    def exclude_process_for_registered_urls(self, request: Request) -> bool:
        url: Any = request.build_absolute_uri()
        for app in self.exclude_urls:
            if app in url:
                return True
        return False

    def include_process_for_registered_urls(self, request: Request) -> bool:
        url: Any = request.build_absolute_uri()
        for app in self.include_urls:
            if app in url:
                return True
        return False

    def before_request(self, request: Request) -> None:
        pass

    def after_request(self, response: Response) -> Response:
        return response


class AuthMiddleware(BaseMiddleware):
    def __init__(
            self,
            exclude_urls: List[str] = [],
            include_urls: List[str] = [],
            *,
            token_cls: TokenInterface,
            user_load: Callable,
            location: str = "header",
            required: bool = True,
    ) -> None:
        super().__init__(exclude_urls, include_urls)
        self.location: str = location
        self.token_cls: TokenInterface = token_cls
        self.user_load: Callable = user_load
        self.required: bool = required

    def get_token(self, request: Request) -> str | None:
        """Get token from request. First check body, then query parameters and then header.

        Args:
            request (Request)

        Returns:
            str | None
        """
        token = None
        if self.location == "body":
            logger.info("Token is in body")
            token: str | None = request.data.get("Authorization", None)  # type: ignore
        elif self.location == "query":
            logger.info("Token is in query")
            token: str | None = request.query_params.get("Authorization", None)  # type: ignore
        elif self.location == "header":
            logger.info("Token is in header")
            token: str | None = request.headers.get("Authorization", None)
        return token

    def authenticate(self, request: Request, token: str) -> Tuple[Any, str] | None:
        """Check token and raise suitable response.

        Args:
            request (Request)
            token (str)

        Raises:
            NotAuthenticated

        Returns:
            Tuple[Any, str] | None
        """
        try:
            claim: Dict = self.token_cls(token)
        except Exception:
            raise NotAuthenticated(detail="Invalid Token")
        user: Any = self.user_load(claim)
        if user:
            return user, token
        else:
            raise NotAuthenticated(detail="Unauthorized")

    def before_request(self, request: Request) -> None:
        token: Optional[str] = self.get_token(request)
        if token:
            result: Tuple[Any, str] | None = self.authenticate(
                request=request, token=token
            )
            if result:
                request.user = result[0]
        elif self.required:
            raise NotAuthenticated(detail="Invalid Token")


class AuthBearerMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.middleware: AuthMiddleware = AuthMiddleware(
            exclude_urls=settings.EXCLUDE_AUTH_URLS,
            include_urls=settings.INCLUDE_AUTH_URLS,
            token_cls=BearerToken(settings.JWT_CONFIGS),
            required=False,
            user_load=user_loader,
        )

    def __call__(self, request) -> Response:
        if self.middleware.include_process_for_registered_urls(
                request
        ) or not self.middleware.exclude_process_for_registered_urls(request):
            self.middleware.before_request(request=request)
        response: Response = self.get_response(request)
        return self.middleware.after_request(response)


class TimezoneMiddleware:
    def __init__(self, get_response):
        logger.info("TimezoneMiddleware:__init__")
        self.get_response = get_response

    def __call__(self, request):
        # logger.info("TimezoneMiddleware:__call__")
        tzname = request.session.get("django_timezone")
        if tzname:
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)


class Middleware:
    class MiddlewareInstaller:
        def __init__(
                self,
                middlewares: List[BaseMiddleware],
                permissions: Any,
        ) -> None:
            logger.info("Middleware:MiddlewareInstaller:__init__")
            self.middlewares: List[BaseMiddleware] = middlewares
            self.permissions: List[BasePermission] = permissions

        def __call__(self, func: Callable) -> Any:
            @wraps(func)
            def wrapper(request: Request, *args: Any, **kwds: Any) -> Response:
                for middleware in self.middlewares:
                    middleware.before_request(request)
                for permission in self.permissions:
                    if not permission.has_permission(request=request, view=func):
                        raise PermissionDenied()
                response: Response = func(request, *args, **kwds)
                for middleware in self.middlewares:
                    response = middleware.after_request(response)
                return response

            return wrapper

    def __new__(
            cls,
            middlewares: Union[BaseMiddleware, List[BaseMiddleware]],
            permissions: Any = [],
    ) -> Any:
        logger.info("Middleware:__new__")
        middleware_installer: Middleware.MiddlewareInstaller = cls.MiddlewareInstaller(
            middlewares=middlewares if isinstance(middlewares, list) else [middlewares],
            permissions=permissions,
        )
        return method_decorator(middleware_installer)


class LanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language = request.META.get("HTTP_C_LANGUAGE", "")
        language = language.split(",")[0].split("-")[0]
        supported_languages = ["fa"]

        if language in supported_languages:
            translation.activate(language)
        else:
            translation.activate("en")

        request.LANGUAGE_CODE = translation.get_language()
