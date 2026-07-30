# inoMS/InteractiveOperations/views.py
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Count

import logging

from core.utils.custom_pagination import StandardResultsSetPagination
from core.auth_tools import permissions
from core.auth_tools.loaders import ActorModel, current_user
from core.responses import Response
from core.open_api import open_api_change_log, open_api_response

from InteractiveOperations import logics, swagger_example_values
from . import models, enums, serializers


logger = logging.getLogger(__name__)

"""
****************************************** Test Api *******************************************************************
"""
class TestToken(APIView):
    permission_classes = [permissions.IsUser]

    def get(self, request, *args, **kwargs):
        user: ActorModel | None = current_user(request=request)
        data = user.jsonifier()

        return Response(
            data=data,
            message='OK',
            status=status.HTTP_200_OK,
        )

class TestApi(APIView):
    # permission_classes = [permissions.IsAdmin]

    @extend_schema(
            tags=["Admin: Test Api - Code:Prf-16"],
        summary="this is sample for create api in django structure",
        description=f"""
           Last Version Update: 1.0.0
           SRS Codes:
           افزودن فرایند
           Adm-Prf-16N4
           Change Log:
           [Explanation about endpoint changes in endpoint]
           {open_api_change_log.test_api}
           -------------------------------------------------------------------------------------------------------------
           Description of endpoint:
           ..................
           
           **Note: 
           - add note for front-end, tester, .....
           - ..............

           """,
        parameters=[ OpenApiParameter(name="actor_type", type=str, required=True, enum=['User', 'Admin', 'University', 'Industry', 'Business']),
                     OpenApiParameter(name="actor_ids", type=str, required=True, default=None), ],
        responses={
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='create instance by model name response',
                examples=[
                    OpenApiExample(
                        'create instance by model name Example',
                        value=swagger_example_values.create_instance_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
    )
    def post(self, request, *args, **kwargs):
        actor_type = self.request.GET.get('actor_type', None)

        actor_ids = self.request.GET.get('actor_ids', None)
        actor_ids = list(map(int, actor_ids.split(',')))

        user: ActorModel | None = current_user(request=request)

        result = logics.TestNameClass.test_function_name(
            actor_id=int(user.id),  # This variable is actually the actor_id of the logged in admin.
            actor_type=actor_type,
            actor_ids=actor_ids,
        )

        return Response(
            message=_('successfully created.'),
            data=result,
            status=status.HTTP_201_CREATED,
        )
     
"""
****************************************** Follow/Unfollow api *******************************************************************
"""
class FollowView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
            tags=["All actor: Follow/unfollow an entitiy - Code: 1-53-1"],
        summary="Follow/Unfollow user/industry/university/business/service/product by actor",
        description=f"""
           Last Version Update: 1.0.0

           SRS Codes: 
           دنبال کردن توسط کاربر یا سرویس دهنده
           USR1-53-1N1, Asr1-53-1N1

           Change Log:
           [Explanation about endpoint changes in endpoint]

           Description of endpoint:
           "Get actor_id, actor_type, target_id, target_type و is_active from user/service provider."
           "If there is no record, create new record. else, is_active will be updated."
           """,
        request=serializers.FollowSerializer,
        responses={
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='Example of follow and unfollow',
                examples=[
                    OpenApiExample(
                        'Correct follow Example',
                        value=swagger_example_values.create_follow_example_successful,
                    ),
                    OpenApiExample(
                        'Correct unfollow Example',
                        value=swagger_example_values.create_unfollow_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        actor_type = serializer.validated_data["actor_type"]     # user / business / university / industry
        actor_id = serializer.validated_data["actor_id"]
        target_type = serializer.validated_data["target_type"]   # user / business / ... / service / product 
        target_id = serializer.validated_data["target_id"]
        is_active = serializer.validated_data.get("is_active", True)

        try:
            actor_group = models.InteractiveRelations._normalize_actor_group(actor_type)
            target_group = models.InteractiveRelations._normalize_target_group(target_type)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model_class = models.InteractiveRelations.FOLLOW_MODEL_MAP.get((actor_group, target_group))
        if not model_class:
            return Response(
                {"detail": "Unsupported actor/target combination."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj, created = model_class.objects.get_or_create(
            actor_id=actor_id,
            actor_type = actor_type,
            target_id=target_id,
            target_type = target_type,
            defaults={"is_active": is_active},
        )
        if not created and obj.is_active != is_active:
            obj.is_active = is_active
            obj.save()

        return Response(serializers.FollowSerializer(obj).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
"""
****************************************** Like/Dislike api *******************************************************************
"""
class LikeView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=["All actor: Like/Dislike an entity - Code: 1-53-1"],
        summary="Like/Dislike user/industry/university/business/service/product/comment by actor",
        description=f"""
           Last Version Update: 1.0.0

           SRS Codes: 
           ایجاد یا تغییر ری اکشن روی یک موجودیت توسط کاربر/سرویس دهنده
           USR1-53-1N2, Asr1-53-1N2, USR1-53-1N3, Asr1-53-1N3
           
           Change Log:
           [Explanation about endpoint changes in endpoint]

           Description of endpoint:
           "Get actor_id, actor_type, target_id, target_type و like_status from user/service provider. "
            "If there is no record, create new record. else, like_status will be updated."
           """,
        request=serializers.LikeSerializer,
        responses={
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description= 'Example for create Like/Dislike or remove reaction on target',
                examples=[
                    OpenApiExample(
                        'Create or update request to create like Example',
                        value=swagger_example_values.create_like_example_successful,
                    ),
                    OpenApiExample(
                        'Create or update request to create dislike Example',
                        value=swagger_example_values.create_dislike_example_successful,
                    ),
                    OpenApiExample(
                        'Update request to remove reaction Example',
                        value=swagger_example_values.update_to_none_reaction_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        actor_type = serializer.validated_data["actor_type"]     # user / business / university / industry
        actor_id = serializer.validated_data["actor_id"]
        target_type = serializer.validated_data["target_type"]   # user / business / ... / service / product / comment
        target_id = serializer.validated_data["target_id"]
        new_status = serializer.validated_data['like_status']    # like / dislike / none

        try:
            actor_group = models.InteractiveRelations._normalize_actor_group(actor_type)
            target_group = models.InteractiveRelations._normalize_target_group(target_type)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model_class = models.InteractiveRelations.LIKE_MODEL_MAP.get((actor_group, target_group))
        if not model_class:
            return Response(
                {"detail": "Unsupported actor/target combination."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj, created = model_class.objects.get_or_create(
            actor_id=actor_id,
            actor_type = actor_type,
            target_id=target_id,
            target_type = target_type,
            defaults={'like_status': new_status},
        )
        if not created:
            old_status = obj.like_status  
            if ((old_status == enums.LikeStatusEnum.LIKE and new_status == enums.LikeStatusEnum.DISLIKE) or
                (old_status == enums.LikeStatusEnum.DISLIKE and new_status == enums.LikeStatusEnum.LIKE)):
                return Response(
                    message=(
                        "You cannot change reaction directly from 'like' to 'dislike' "
                        "or vice versa. First set like_status=2, then send a new request."
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if old_status != new_status:
                obj.like_status = new_status
                obj.save()

        return Response(serializers.LikeSerializer(obj).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
"""
****************************************** Share api *******************************************************************
"""
class ShareView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=["All actor: Share entity - Code: 1-53-1"],
        summary="Share user/industry/university/business/service/product page by actor",
        description=f"""
           Last Version Update: 1.0.0

           SRS Codes:
           به اشتراک گذاری در سایت 
           USR1-53-1N4, Asr1-53-1N4 
           به اشتراک گذاری در دیگر پلتفرم ها
           USR1-53-1N5, Asr1-53-1N5
           
           Change Log:
           [Explanation about endpoint changes in endpoint]
           
           Description of endpoint:
           "Get actor_id, actor_type, target_id, target_type, platform, destination_type و destination_id, url, reason from user/service provider."
            "Create new record."
            "destination_id, destination_type and reason could be null."
           """,
        request = serializers.ShareSerializer,
        responses={
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='Example to create Share base on platform',
                examples=[
                    OpenApiExample(
                        'Create share in site Example',
                        value=swagger_example_values.create_share_in_site_with_reason_example_successful,
                    ),
                    OpenApiExample(
                        'Create share in site without reason Example',
                        value=swagger_example_values.create_share_in_site_without_reason_example_successful,
                    ),
                    OpenApiExample(
                        'Create share to telegram app Example',
                        value=swagger_example_values.create_share_on_telegram_example_successful,
                    ),
                    OpenApiExample(
                        'Create share to whatsapp app Example',
                        value=swagger_example_values.create_share_on_whatsapp_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False 
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.ShareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        actor_type = serializer.validated_data["actor_type"]     # user / business / university / industry
        actor_id = serializer.validated_data["actor_id"]
        target_type = serializer.validated_data["target_type"]   # user / business / ... / service / product / comment
        target_id = serializer.validated_data["target_id"]
        platform = serializer.validated_data['platform']
        destination_type = serializer.validated_data.get('destination_type', None)
        destination_id = serializer.validated_data.get('destination_id', None)
        url = serializer.validated_data.get('url')
        reason = serializer.validated_data.get('reason', None)

        try:
            actor_group = models.InteractiveRelations._normalize_actor_group(actor_type)
            target_group = models.InteractiveRelations._normalize_target_group(target_type)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model_class = models.InteractiveRelations.SHARE_MODEL_MAP.get((actor_group, target_group))
        if not model_class:
            return Response(
                {"detail": "Unsupported actor/target combination."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        obj = model_class.objects.create(
            actor_id=actor_id,
            actor_type=actor_type,
            target_id=target_id,
            target_type=target_type,
            platform=platform,
            destination_type=destination_type,
            destination_id=destination_id,
            url=url,
            reason=reason,
        )

        return Response(serializers.ShareSerializer(obj).data, status=status.HTTP_201_CREATED)
"""
****************************************** Score api *******************************************************************
"""
class ScoreView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=["All actor: Score entity - Code: 1-53-1"],
        summary="Score to industry/university/business/service/product by actor",
        description=f"""
        Last Version Update: 1.0.0

        SRS Codes:
        امتیازدهی به موجودیت توسط کاربر یا سرویس دهنده
        Usr1-53-1N6, Asr1-53-1N6

        Change Log:
        [Explanation about endpoint changes in endpoint]
        
        Description of endpoint:
        "Get actor_id, actor_type, target_id, target_type و score from user/service provider. "
        "If there is no record, creates new record. else, score will be updated."
        """,
        request=serializers.ScoreSerializer,
        responses={
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='Example to score to',
                examples=[
                    OpenApiExample(
                        'create score Example',
                        value=swagger_example_values.create_score_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.ScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        actor_type = serializer.validated_data["actor_type"]     # user / business / university / industry
        actor_id = serializer.validated_data["actor_id"]
        target_type = serializer.validated_data["target_type"]   # business / ... / service / product 
        target_id = serializer.validated_data["target_id"]
        score = serializer.validated_data['score']

        try:
            actor_group = models.InteractiveRelations._normalize_actor_group(actor_type)
            target_group = models.InteractiveRelations._normalize_target_group(target_type)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model_class = models.InteractiveRelations.SCORE_MODEL_MAP.get((actor_group, target_group))
        if not model_class:
            return Response(
                {"detail": "Unsupported actor/target combination."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj, created = model_class.objects.get_or_create(
            actor_id=actor_id,
            actor_type = actor_type,
            target_id=target_id,
            target_type = target_type,
            defaults={'score': score},
        )
        if not created:
            obj.score = score
            obj.save()

        return Response(serializers.ScoreSerializer(obj).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
"""
****************************************** Average score (get) api *******************************************************************
"""
class ScoreAverageView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=["All actor: Score entity - Code: 1-53-1"],
        summary="View Average score of industry/university/business/service/product",
        description=f"""  
        Last Version Update: 1.0.0

        SRS Codes:
        مشاهده میانگین امتیازات موجودیت توسط کاربر/سرویس دهنده
        USR1-53-1N7, Asr1-53-1N7

        Change Log:
        [Explanation about endpoint changes in endpoint]
                
        Description of endpoint:
        "Get target_id, target_type from user/service provider. "
        "If there is no record, returns none. else, it shows average score and number of scorers of an entity."
        """,
        parameters=[
            OpenApiParameter(name="target_type", required=True, type=str, enum=serializers.ScoreAverageSerializer.TARGET_TYPE_ENUM_SCORE_PARAM),
            OpenApiParameter(name="target_id", required=True, type=int, description="Entity ID",), ],
        request=None,
        responses={
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='Example to fetch Average score of entity',
                examples=[
                    OpenApiExample(
                        'Fetch average score Example',
                        value=swagger_example_values.get_average_score_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False
    )
    def get(self, request, *args, **kwargs):
        target_type = request.query_params.get("target_type")
        target_id = request.query_params.get("target_id")

        if not target_type or not target_id:
            return Response(
                {"detail": "target_type and target_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            target_type_int = int(target_type)
            target_id = int(target_id)
        except (TypeError, ValueError):
            return Response(
                {"message": "target_type and target_id must be int.",},status=status.HTTP_400_BAD_REQUEST,
            )

        target_type_str = enums.TARGET_TYPE_INT_TO_STR.get(target_type_int)
        if target_type_str is None:
            return Response(
                {"message": f"Unsupported target_type: {target_type_int}",},status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            target_group = models.InteractiveRelations._normalize_target_group(target_type_str)
        except ValueError as e:
            return Response({"message": str(e),},status=status.HTTP_400_BAD_REQUEST,)
        
        model_classes = models.InteractiveRelations.SCORE_AVERAGE_MAP.get(target_group)
        if not model_classes:
            return Response({"detail": f"Unsupported target_type: {target_type_int}",},status=status.HTTP_400_BAD_REQUEST,)

        total_score = 0
        total_count = 0
        for model in model_classes:
            qs = model.objects.filter(
                target_type=target_type,
                target_id=target_id,
            )
            agg = qs.aggregate(
                sum_score=Sum("score"),
                count_score=Count("id"),
            )
            if agg["sum_score"] is not None:
                total_score += agg["sum_score"]
                total_count += agg["count_score"]
        avg_value = (total_score / total_count) if total_count else None

        response_data = {
            "target_type": target_type,
            "target_id": int(target_id),
            "score": avg_value,
            "count": total_count,
        }
        return Response(response_data, status=status.HTTP_200_OK)
"""
****************************************** Followers list api *******************************************************************
"""
class FollowersListView(APIView, PageNumberPagination):
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    @extend_schema(
        tags=["All actor: Follow List - Code: 1-53-1"],
        summary="Get followers list of user/industry/university/business/service/product by actor",
        description=f"""
        Last Version Update: 1.0.0

        SRS Codes: 
        مشاهده لیست دنبال کنندگان یک موجودیت توسط کاربر/سرویس دهنده
        USR1-53-1N8, Asr1-53-1N8

        Change Log:
        [Explanation about endpoint changes in endpoint]

        Description of endpoint:
        "Get target_id, target_type from user/service provider. "
        "api returns list of followers of entity."
        """,
        parameters=[
            OpenApiParameter(name="target_type", required=True, type=int, enum=serializers.FollowSerializer.TARGET_TYPE_ENUM_FOLLOW_PARAM),
            OpenApiParameter(name="target_id", required=True, type=int, description="target's ID",), ],
        responses={
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='Example to fetch List of followers.',
                examples=[
                    OpenApiExample(
                        'Fetch list of followers of entity Example',
                        value=swagger_example_values.get_followers_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False
    )
    def get(self, request, *args, **kwargs):
        target_type = request.query_params.get("target_type")
        target_id = request.query_params.get("target_id")

        if target_type is None or target_id is None:
            return Response({"message": "target_type and target_id are required.",},
                            status=status.HTTP_400_BAD_REQUEST,)

        try:
            target_type_int = int(target_type)
            target_id = int(target_id)
        except (TypeError, ValueError):
            return Response({"message": "target_type and target_id must be int.",},
                status=status.HTTP_400_BAD_REQUEST,)

        target_type_str = enums.TARGET_TYPE_INT_TO_STR.get(target_type_int)
        if target_type_str is None:
            return Response(
                {"message": f"Unsupported target_type: {target_type_int}",},
                status=status.HTTP_400_BAD_REQUEST,)

        try:
            target_group = models.InteractiveRelations._normalize_target_group(target_type_str)
        except ValueError as e:
            return Response({"message": str(e),},
                            status=status.HTTP_400_BAD_REQUEST,)

        model_classes = models.InteractiveRelations.FOLLOWER_LIST_MAP.get(target_group)
        if not model_classes:
            return Response({"message": f"Unsupported target_type: {target_type_int}",},
                            status=status.HTTP_400_BAD_REQUEST,)

        followers = []
        for model_class in model_classes:
            qs = model_class.objects.filter(
                target_type=target_type_int,
                target_id=target_id,
                is_active=True,
            ).order_by("-last_updated_at")
            for f in qs:
                followers.append({
                    "actor_type": f.actor_type,
                    "actor_id": f.actor_id,
                    "last_updated_at": f.last_updated_at,
                })
        data = {
            "target_type": target_type_int,
            "target_id": target_id,
            "count": len(followers),
            "results": followers,
        }
        return Response(serializers.FollowersListSerializer(data).data, status=status.HTTP_200_OK)
"""
****************************************** Followings list api *******************************************************************
"""
class FollowingsListView(APIView, PageNumberPagination):
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    @extend_schema(
        tags=["All actor: Follow List - Code: 1-53-1"],
        summary="Get followings list of user/industry/university/business by actor",
        description=f"""
        Last Version Update: 1.0.0

        SRS Codes: 
        مشاهده لیست دنبال شدگان توسط یک موجودیت توسط کاربر/سرویس دهنده
        USR1-53-1N9, Asr1-53-1N9

        Change Log:
        [Explanation about endpoint changes in endpoint]

        Description of endpoint:
        "Get actor_id, actor_type from user/service provider. "
        "api returns list of followings of entity."
        """,
        parameters=[
            OpenApiParameter(name="actor_type", required=True, type=int, enum=serializers.FollowSerializer.ACTOR_TYPE_ENUM_FOLLOW_PARAM),
            OpenApiParameter(name="actor_id", required=True, type=int, description="actor's ID",), ],
        responses={
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='Example to fetch followings list',
                examples=[
                    OpenApiExample(
                        'Fetch list of followings of entity Example.',
                        value=swagger_example_values.get_followings_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False
    )
    def get(self, request, *args, **kwargs):
        actor_type = request.query_params.get("actor_type")
        actor_id = request.query_params.get("actor_id")

        if actor_type is None or actor_id is None:
            return Response({"message": "actor_type and actor_id are required.",},
                            status=status.HTTP_400_BAD_REQUEST,)

        try:
            actor_type_int = int(actor_type)
            actor_id = int(actor_id)
        except (TypeError, ValueError):
            return Response({"message": "actor_type and actor_id must be int.",},
                status=status.HTTP_400_BAD_REQUEST,)

        actor_type_str = enums.ACTOR_TYPE_INT_TO_STR.get(actor_type_int)
        if actor_type_str is None:
            return Response(
                {"message": f"Unsupported target_type: {actor_type_int}",},
                            status=status.HTTP_400_BAD_REQUEST,)

        try:
            actor_group = models.InteractiveRelations._normalize_actor_group(actor_type_str)
        except ValueError as e:
            return Response({"message": str(e),},
                            status=status.HTTP_400_BAD_REQUEST,)

        model_classes = models.InteractiveRelations.FOLLOWING_LIST_MAP.get(actor_group)
        if not model_classes:
            return Response({"message": f"Unsupported target_type: {actor_type_int}",},
                            status=status.HTTP_400_BAD_REQUEST,)

        followings = []
        for model_class in model_classes:
            qs = model_class.objects.filter(
                actor_type=actor_type,
                actor_id=actor_id,
                is_active=True,
            ).order_by("-last_updated_at")
            for f in qs:
                followings.append({
                    "target_type": f.target_type,
                    "target_id": f.target_id,
                    "last_updated_at": f.last_updated_at,

                })
        data = {
            "actor_type": actor_type,
            "actor_id": int(actor_id),
            "count": len(followings),
            "results": followings,
        }
        return Response(serializers.FollowingsListSerializer(data).data, status=status.HTTP_200_OK)
"""
****************************************** Likers list api *******************************************************************
"""
class LikersListView(APIView, PageNumberPagination):
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    @extend_schema(
        tags=["All actor: Like List - Code: 1-53-1"],
        summary="Get likers list of user/industry/university/business/service/product/comment by actor",
        parameters=[
            OpenApiParameter(name="target_type",required=True,type=int,enum=serializers.LikeSerializer.TARGET_TYPE_ENUM_LIKE_PARAM,),
            OpenApiParameter(name="target_id",required=True,type=int,description="target's ID",),
        ],
        responses = {
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='Example to fetch likers list',
                examples=[
                    OpenApiExample(
                        'Fetch list of likers of entity Example',
                        value=swagger_example_values.get_likers_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False
    )
    def get(self, request, *args, **kwargs):
        target_type = request.query_params.get("target_type")
        target_id = request.query_params.get("target_id")

        if target_type is None or target_id is None:
            return Response({"message": "target_type and target_id are required.",},
                status=status.HTTP_400_BAD_REQUEST,)

        try:
            target_type_int = int(target_type)
            target_id = int(target_id)
        except (TypeError, ValueError):
            return Response({"message": "target_type and target_id must be int.",},
                    status=status.HTTP_400_BAD_REQUEST,)

        # out of range of our enums
        target_type_str = enums.TARGET_TYPE_INT_TO_STR.get(target_type_int)
        if target_type_str is None:
            return Response({"message": f"Unsupported target_type: {target_type_int}",},
                status=status.HTTP_400_BAD_REQUEST,)

        # find the group of actor/target (groups: user->user , bus/ind/uni->serviceProvider , service/product/comment->others)
        try:
            target_group = models.InteractiveRelations._normalize_target_group(target_type_str)
        except ValueError as e:
            return Response({"message": str(e),},
                status=status.HTTP_400_BAD_REQUEST,)
        # get related models
        model_classes = models.InteractiveRelations.LIKER_LIST_MAP.get(target_group)
        if not model_classes:
            return Response({"message": f"Unsupported target_type: {target_type_int}",},
                status=status.HTTP_400_BAD_REQUEST,)

        #search and append
        likers = []
        for model_class in model_classes:
            qs = model_class.objects.filter(
                target_type=target_type_int,
                target_id=target_id,
                like_status=enums.LikeStatusEnum.LIKE,
            ).order_by("-last_updated_at")

            for obj in qs:
                likers.append({
                    "actor_type": obj.actor_type,
                    "actor_id": obj.actor_id,
                    "last_updated_at": obj.last_updated_at,
                })

        # pass data to serializer
        data = {
            "target_type": target_type_int,
            "target_id": target_id,
            "count": len(likers),
            "results": likers,
        }

        return Response(serializers.LikersListSerializer(data).data,status=status.HTTP_200_OK,)
"""
****************************************** Likees list api *******************************************************************
"""
class LikeesListView(APIView, PageNumberPagination):
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    @extend_schema(
        tags=["All actor: Like List - Code: 1-53-1"],
        summary="Get likees list of user/industry/university/business by actor",
        description=f"""
        Last Version Update: 1.0.0

        SRS Codes: 
        مشاهده لیست پسند شدگان توسط یک موجودیت توسط کاربر/سرویس دهنده
        USR1-53-1N11, Asr1-53-1N11

        Change Log:
        [Explanation about endpoint changes in endpoint]

        Description of endpoint:
        "Get actor_id, actor_type from user/service provider. "
        "api returns list of likees of entity."
        """,
        parameters=[
            OpenApiParameter(name="actor_type", required=True, type=int, enum=serializers.LikeSerializer.ACTOR_TYPE_ENUM_LIKE_PARAM),
            OpenApiParameter(name="actor_id", required=True, type=int, description="actor's ID",), ],
        request = None,
        responses = {
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='Example to fetch likees list',
                examples=[
                    OpenApiExample(
                        'Fetch list of likees of actor Example',
                        value=swagger_example_values.get_likees_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False
    )
    def get(self, request, *args, **kwargs):
        actor_type = request.query_params.get("actor_type")
        actor_id = request.query_params.get("actor_id")

        if actor_type is None or actor_id is None:
            return Response({"message": "actor_type and actor_id are required.",},
                            status=status.HTTP_400_BAD_REQUEST,)

        try:
            actor_type_int = int(actor_type)
            actor_id = int(actor_id)
        except (TypeError, ValueError):
            return Response({"message": "actor_type and actor_id must be int.",},
                status=status.HTTP_400_BAD_REQUEST,)

        actor_type_str = enums.ACTOR_TYPE_INT_TO_STR.get(actor_type_int)
        if actor_type_str is None:
            return Response(
                {"message": f"Unsupported target_type: {actor_type_int}",},
                            status=status.HTTP_400_BAD_REQUEST,)

        try:
            actor_group = models.InteractiveRelations._normalize_actor_group(actor_type_str)
        except ValueError as e:
            return Response({"message": str(e),},
                            status=status.HTTP_400_BAD_REQUEST,)

        model_classes = models.InteractiveRelations.LIKEE_LIST_MAP.get(actor_group)
        if not model_classes:
            return Response({"message": f"Unsupported target_type: {actor_type_int}",},
                            status=status.HTTP_400_BAD_REQUEST,)

        likees = []
        for model_class in model_classes:
            qs = model_class.objects.filter(
                actor_type=actor_type,
                actor_id=actor_id,
                like_status = enums.LikeStatusEnum.LIKE
            ).order_by("-last_updated_at")
            for f in qs:
                likees.append({
                    "target_type": f.target_type,
                    "target_id": f.target_id,
                    "last_updated_at": f.last_updated_at,
                })
        data = {
            "actor_type": actor_type,
            "actor_id": int(actor_id),
            "count": len(likees),
            "results": likees,
        }
        return Response(serializers.LikeesListSerializer(data).data, status=status.HTTP_200_OK)
"""
****************************************** Dislikers list api *******************************************************************
"""
class DislikersListView(APIView, PageNumberPagination):
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    @extend_schema(
        tags=["All actor: Dislike List - Code: 1-53-1"],
        summary="Get dislikers list of user/industry/university/business/service/product/comment by actor",
        description=f"""
        Last Version Update: 1.0.0

        SRS Codes: 
        مشاهده لیست نسپند کنندگان یک موجودیت توسط کاربر/سرویس دهنده
        USR1-53-1N12, Asr1-53-1N12

        Change Log:
        [Explanation about endpoint changes in endpoint]

        Description of endpoint:
        "Get target_id, target_type from user/service provider. "
        "api returns list of dislikers of entity."
        """,
        parameters=[
            OpenApiParameter(name="target_type", required=True, type=int, enum=serializers.LikeSerializer.TARGET_TYPE_ENUM_LIKE_PARAM),
            OpenApiParameter(name="target_id", required=True, type=int, description="targets's ID",), ],
        request = None,
        responses = {
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='Example to fetch dislikers list',
                examples=[
                    OpenApiExample(
                        'Fetch list of dislikers of entity Example',
                        value=swagger_example_values.get_dislikers_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False
    )
    def get(self, request, *args, **kwargs):
        target_type = request.query_params.get("target_type")
        target_id = request.query_params.get("target_id")

        if target_type is None or target_id is None:
            return Response({"message": "target_type و target_id الزامی هستند.",},
                status=status.HTTP_400_BAD_REQUEST,)

        try:
            target_type_int = int(target_type)
            target_id = int(target_id)
        except (TypeError, ValueError):
            return Response({"message": "target_type و target_id باید عدد صحیح باشند.",},
                    status=status.HTTP_400_BAD_REQUEST,)

        target_type_str = enums.TARGET_TYPE_INT_TO_STR.get(target_type_int)
        if target_type_str is None:
            return Response({"message": f"Unsupported target_type: {target_type_int}",},
                status=status.HTTP_400_BAD_REQUEST,)

        try:
            target_group = models.InteractiveRelations._normalize_target_group(target_type_str)
        except ValueError as e:
            return Response({"message": str(e),},
                status=status.HTTP_400_BAD_REQUEST,)

        model_classes = models.InteractiveRelations.LIKER_LIST_MAP.get(target_group)
        if not model_classes:
            return Response({"message": f"Unsupported target_type: {target_type_int}",},
                status=status.HTTP_400_BAD_REQUEST,)

        dislikers = []
        for model_class in model_classes:
            qs = model_class.objects.filter(
                target_type=target_type,
                target_id=target_id,
                like_status=enums.LikeStatusEnum.DISLIKE,
            ).order_by("-last_updated_at")
            for f in qs:
                dislikers.append({
                    "actor_type": f.actor_type,
                    "actor_id": f.actor_id,
                    "last_updated_at": f.last_updated_at,
                })
        data = {
            "target_type": target_type,
            "target_id": int(target_id),
            "count": len(dislikers),
            "results": dislikers,
        }
        return Response(serializers.DislikersListSerializer(data).data, status=status.HTTP_200_OK)
"""
****************************************** Dislikees list api *******************************************************************
"""
class DislikeesListView(APIView, PageNumberPagination):
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    @extend_schema(
        tags=["All actor: Dislike List - Code: 1-53-1"],
        summary="Get dislikees list of user/industry/university/business by actor",
        description=f"""
        Last Version Update: 1.0.0

        SRS Codes: 
        مشاهده لیست نپسند شدگان توسط یک موجودیت توسط کاربر/سرویس دهنده
        USR1-53-1N13, Asr1-53-1N13

        Change Log:
        [Explanation about endpoint changes in endpoint]

        Description of endpoint:
        "Get actor_id, actor_type from user/service provider. "
        "api returns list of dislikees of entity."
        """,
        parameters=[
            OpenApiParameter(name="actor_type", required=True, type=int, enum=serializers.LikeSerializer.ACTOR_TYPE_ENUM_LIKE_PARAM),
            OpenApiParameter(name="actor_id", required=True, type=int, description="actor's ID",), ],
        request = None,
        responses = {
            200: OpenApiResponse(
                response=serializers.NameResponseSerializer,
                description='Example to fetch dislikees list',
                examples=[
                    OpenApiExample(
                        'Fetch list of dislikees of entity Example',
                        value=swagger_example_values.get_dislikees_example_successful,
                    ),
                ],
            ),
            400: open_api_response.responses_400,
            500: open_api_response.responses_500,
        },
        deprecated=False
    )
    def get(self, request, *args, **kwargs):
        actor_type = request.query_params.get("actor_type")
        actor_id = request.query_params.get("actor_id")

        if actor_type is None or actor_id is None:
            return Response({"message": "actor_type and actor_id are required.",},
                            status=status.HTTP_400_BAD_REQUEST,)

        try:
            actor_type_int = int(actor_type)
            actor_id = int(actor_id)
        except (TypeError, ValueError):
            return Response({"message": "actor_type and actor_id must be int.",},
                status=status.HTTP_400_BAD_REQUEST,)

        actor_type_str = enums.ACTOR_TYPE_INT_TO_STR.get(actor_type_int)
        if actor_type_str is None:
            return Response(
                {"message": f"Unsupported target_type: {actor_type_int}",},
                            status=status.HTTP_400_BAD_REQUEST,)

        try:
            actor_group = models.InteractiveRelations._normalize_actor_group(actor_type_str)
        except ValueError as e:
            return Response({"message": str(e),},
                            status=status.HTTP_400_BAD_REQUEST,)

        model_classes = models.InteractiveRelations.LIKEE_LIST_MAP.get(actor_group)
        if not model_classes:
            return Response({"message": f"Unsupported target_type: {actor_type_int}",},
                            status=status.HTTP_400_BAD_REQUEST,)

        dislikees = []
        for model_class in model_classes:
            qs = model_class.objects.filter(
                actor_type=actor_type,
                actor_id=actor_id,
                like_status = enums.LikeStatusEnum.DISLIKE
            ).order_by("-last_updated_at")
            for f in qs:
                dislikees.append({
                    "target_type": f.target_type,
                    "target_id": f.target_id,
                    "last_updated_at": f.last_updated_at,
                })
        data = {
            "actor_type": actor_type,
            "actor_id": int(actor_id),
            "count": len(dislikees),
            "results": dislikees,
        }
        return Response(serializers.DislikeesListSerializer(data).data, status=status.HTTP_200_OK)