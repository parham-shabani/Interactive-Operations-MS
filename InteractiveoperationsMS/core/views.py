from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from core.auth_tools import permissions
from core.auth_tools.loaders import ActorModel, current_user
from core.responses import Response
import logging

logger = logging.getLogger(__name__)

# Create your views here.

"""
****************************************** Test Token *****************************************************************
"""


class TestToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["All Actor: Test Token"],
        summary="test token",
        description="""
        Test token
        """,
        request=None,
        responses=None,
    )
    def get(self, request, *args, **kwargs):
        user: ActorModel | None = current_user(request=request)
        data = user.jsonifier()

        return Response(
            data=data,
            message='OK',
            status=status.HTTP_200_OK,
        )
