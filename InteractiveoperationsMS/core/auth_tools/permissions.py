from rest_framework.request import Request
from rest_framework.permissions import BasePermission
from core.auth_tools.loaders import ActorModel
from core.auth_tools.loaders import user_proxy_checking
import logging

logger = logging.getLogger(__name__)


# TODO: MODIFY FOR YOUR PROJECT

class OrPermission:
    @classmethod
    def Or(cls, *permission_classes: type[BasePermission]) -> type[BasePermission]:
        class CombinedPermission(BasePermission):
            def __init__(self):
                self.permission_classes = [perm() for perm in permission_classes]

            def has_permission(self, request, view):
                return any(
                    permission.has_permission(request, view)
                    for permission in self.permission_classes
                )

            def has_object_permission(self, request, view, obj):
                return any(
                    permission.has_object_permission(request, view, obj)
                    for permission in self.permission_classes
                )

        return CombinedPermission


class IsAnonymous(BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return True


class IsAuthenticated(BasePermission):
    @user_proxy_checking
    def has_permission(self, request: Request, view) -> bool:
        user_permission: ActorModel = request.user
        return (
                (
                        user_permission.profile.permissions.is_user
                        and user_permission.profile.type == 1
                )
                or (
                        user_permission.profile.permissions.is_admin
                        and user_permission.profile.type == 2
                )
                or (
                        user_permission.profile.permissions.is_university
                        and user_permission.profile.type == 4
                )
                or (
                        user_permission.profile.permissions.is_industry
                        and user_permission.profile.type == 5
                )
                or (
                        user_permission.profile.permissions.is_business
                        and user_permission.profile.type == 6
                )
        )


class IsActor(BasePermission):
    @user_proxy_checking
    def has_permission(self, request: Request, view) -> bool:
        user_permission: ActorModel = request.user
        return (
                (
                        user_permission.profile.permissions.is_user
                        and user_permission.profile.type == 1
                )
                or (
                        user_permission.profile.permissions.is_university
                        and user_permission.profile.type == 4
                )
                or (
                        user_permission.profile.permissions.is_industry
                        and user_permission.profile.type == 5
                )
                or (
                        user_permission.profile.permissions.is_business
                        and user_permission.profile.type == 6
                )
        )


class IsUser(BasePermission):
    @user_proxy_checking
    def has_permission(self, request: Request, view) -> bool:
        user_permission: ActorModel = request.user
        return (
                user_permission.profile.permissions.is_user
                and user_permission.profile.type == 1
        )


class IsAdmin(BasePermission):
    @user_proxy_checking
    def has_permission(self, request: Request, view) -> bool:
        user_permission: ActorModel = request.user
        return (
                user_permission.profile.permissions.is_admin
                and user_permission.profile.type == 2
        )


class IsTopAdmin(BasePermission):
    @user_proxy_checking
    def has_permission(self, request: Request, view) -> bool:
        user_permission: ActorModel = request.user
        return (
                user_permission.profile.permissions.is_admin
                and user_permission.profile.type == 2
                and int(user_permission.id) == 2
        )


class IsUniversity(BasePermission):
    @user_proxy_checking
    def has_permission(self, request: Request, view) -> bool:
        user_permission: ActorModel = request.user
        return (
                user_permission.profile.permissions.is_university
                and user_permission.profile.type == 4
        )


class IsIndustry(BasePermission):
    @user_proxy_checking
    def has_permission(self, request: Request, view) -> bool:
        user_permission: ActorModel = request.user
        return (
                user_permission.profile.permissions.is_industry
                and user_permission.profile.type == 5
        )


class IsBusiness(BasePermission):
    @user_proxy_checking
    def has_permission(self, request: Request, view) -> bool:
        user_permission: ActorModel = request.user
        return (
                user_permission.profile.permissions.is_business
                and user_permission.profile.type == 6
        )
