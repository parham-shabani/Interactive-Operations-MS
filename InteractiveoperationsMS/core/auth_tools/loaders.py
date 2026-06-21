from dataclasses import KW_ONLY, dataclass, field
from functools import wraps
from typing import Dict
from rest_framework.request import Request
from rest_framework.exceptions import NotAuthenticated
import logging

logger = logging.getLogger(__name__)


class BaseModel:
    def jsonifier(self) -> Dict[str, str]:
        fields: Dict[str, BaseModel] = self.__dict__
        row: Dict = dict()
        for key, field in fields.items():
            row[key] = field if not isinstance(field, BaseModel) else field.jsonifier()
        return row


@dataclass
class ActorPermissions(BaseModel):
    # TODO: MODIFY FOR YOUR PROJECT
    is_user: bool
    is_admin: bool
    is_university: bool
    is_industry: bool
    is_business: bool


@dataclass
class ActorProfile(BaseModel):
    email: str | None
    phone: str | None
    type: int
    permissions: ActorPermissions


@dataclass
class ActorModel(BaseModel):
    id: int = field(init=False)
    _: KW_ONLY
    sub: str | int
    name: str | None
    profile: ActorProfile

    def __post_init__(self) -> None:
        self.id = int(self.sub)
        self.profile.type = int(self.profile.type)


@dataclass
class SupporterModel:
    id: str | int = field(init=False)
    _: KW_ONLY
    sub: str | int
    name: str

    def __post_init__(self) -> None:
        self.id = self.sub


def supporter_loader(data: Dict) -> SupporterModel:
    return SupporterModel(sub=data["sub"], name=data["name"])


def user_loader(data: Dict) -> ActorModel:
    return ActorModel(
        sub=data["sub"],
        name=data["name"],
        profile=ActorProfile(
            email=data["profile"]["email"],
            phone=data["profile"]["phone"],
            type=data["profile"]["type"],
            permissions=ActorPermissions(**data["profile"]["permissions"]),
        ),
    )


def registered_user_loader(actor_id: int | str, actor_type: str):
    # from core import utils as core_utils
    # MyModelNameActor = core_utils.ModelsActorTypeClass.get_actor_model_map(
    #     actor_type=actor_type, is_unreg_model=False)
    # actor: MyModelNameActor = MyModelNameActor.objects.filter(pk=actor_id).first()
    # if actor:
    #     return actor
    # raise NotAuthenticated()

    # TODO: Comment out the above code in other microservices and use the following section instead:
    """
    This function should be implemented by developer

    Args:
        actor_id (int | str): actor id

    Returns:
        Any: User model object
    """
    raise NotImplementedError


def current_registered_user(request: Request, actor_type: str):
    actor: ActorModel | None = current_user(request=request)
    if actor:
        return registered_user_loader(actor_id=actor.id, actor_type=actor_type)
    return None


def current_user(request: Request) -> ActorModel | None:
    if isinstance(request.user, ActorModel):
        return request.user
    return None


def current_supporter(request: Request) -> SupporterModel | None:
    user: ActorModel | None = current_user(request=request)
    if user:
        return supporter_loader(user.jsonifier())
    return None


def user_proxy_checking(func):
    @wraps(func)
    def wrapper(self, request: Request, *args, **kwargs):
        if not current_user(request=request):
            logger.info("Start wrapper")
            raise NotAuthenticated()
        return func(self, request, *args, **kwargs)

    return wrapper
