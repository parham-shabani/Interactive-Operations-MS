# inoMS/core/auth_tools/authentication.py
from typing import Any, Callable, Dict, List, Optional, Tuple
from rest_framework import authentication
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from django.conf import settings
from core.extensions.jwt.interfaces import TokenInterface
from core.auth_tools.loaders import user_loader
from core.extensions.jwt.tokens import BearerToken


class OAuth2BearerAuthentication(authentication.BaseAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """

    www_authenticate_realm: str = "api"
    media_type: str = "application/json"

    def __init__(
            self,
            token_cls: TokenInterface = BearerToken(settings.JWT_CONFIGS),
            user_load: Callable = user_loader,
            location: str = "header",
            required: bool = False,
    ) -> None:
        self.location: str = location
        self.exclude_urls: List[str] = settings.EXCLUDE_AUTH_URLS
        self.include_urls: List[str] = settings.INCLUDE_AUTH_URLS
        self.token_cls: TokenInterface = token_cls
        self.user_load: Callable = user_load
        self.required: bool = required

    def exclude_process_for_registered_urls(self, request: Request) -> bool:
        """Exclude authentication process for registered urls

        Args:
            request (Request)

        Returns:
            bool
        """
        url: str = request.build_absolute_uri()
        for app in self.exclude_urls:
            if app in url:
                return True
        return False

    def include_process_for_registered_urls(self, request: Request) -> bool:
        """Include authentication process for registered urls

        Args:
            request (Request)

        Returns:
            bool
        """
        url: str = request.build_absolute_uri()
        for app in self.include_urls:
            if app in url:
                return True
        return False

    def get_token(self, request: Request) -> str | None:
        """Get token from the request. First check body, then query parameters and then header.

        Args:
            request (Request)

        Returns:
            str | None
        """
        token = None
        if self.location == "body":
            token: str | None = request.data.get("Authorization", None)
        elif self.location == "query":
            token: str | None = request.query_params.get("Authorization", None)
        elif self.location == "header":
            token: str | None = request.headers.get("Authorization", None)
        return token

    def authenticate(self, request: Request) -> Tuple[Any, str] | None:
        """Authenticate user

        Args:
            request (Request)

        Raises:
            NotAuthenticated
            NotAuthenticated
            NotAuthenticated

        Returns:
            Tuple[Any, str] | None
        """
        if self.has_allow_any_permission(request):
            return None
        if not self.exclude_process_for_registered_urls(request):
            token: Optional[str] = self.get_token(request)
            if token:
                try:
                    claim: Dict = self.token_cls(token)
                except Exception:
                    raise NotAuthenticated(detail="Invalid Token")
                user: Any = self.user_load(claim)
                if user:
                    return user, token
                else:
                    raise NotAuthenticated(detail="Unauthorized")
            elif self.required:
                raise NotAuthenticated(detail="Invalid Token")

    def authenticate_header(self, request: Request) -> str:
        return '{} realm="{}"'.format(
            "Bearer",
            self.www_authenticate_realm,
        )

    def has_allow_any_permission(self, request: Request) -> bool:
        """
        Check if the view associated with the request has the AllowAny permission.
        """
        view = request.resolver_match.func.cls
        return any(
            isinstance(permission(), AllowAny)
            for permission in getattr(view, "permission_classes", [])
        )
