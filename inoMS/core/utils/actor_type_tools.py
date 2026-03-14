from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from core import enums
from core.exceptions import exceptions as base_exceptions
from core.auth_tools.loaders import ActorModel, current_user
import logging

logger = logging.getLogger(__name__)
load_dotenv()

"""
****************************************** Models/Actor Info and Token ************************************************
"""


class ModelsActorTypeClass:
    pass


class ActorInfo:
    """
    Get actor info and check token
    """

    @classmethod
    def get_actor_info_from_token(cls, request):
        """
        Extract actor info from user token.
        """
        logger.info(f"ActorInfo:get_actor_info_from_token")

        actor_type = request.GET.get('actor_type', None)

        # Get user from token
        user: ActorModel | None = current_user(request=request)
        user_data = user.jsonifier()
        user_type_id = int(user_data["profile"]['type'])
        # user_type = enums.ACTOR_TYPE_DICT[user_type_id]
        user_type = enums.ACTOR_ID_TO_LABEL.get(user_type_id)
        if actor_type != user_type:
            raise base_exceptions.APIException(detail='Invalid token type')

        print(f"user, actor_type:{user, actor_type}")
        return user, actor_type
