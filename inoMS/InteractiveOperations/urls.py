# InteractiveOperations/urls.py
from django.urls import path
from . import views
from .views import FollowersListView, FollowingsListView, LikersListView, LikeesListView, DislikersListView, DislikeesListView


app_name = 'interactive_operations'

urlpatterns = [
    path('test_api', views.TestApi.as_view(), name='test_api'),
    path('follow', views.FollowView.as_view(), name='follow'),
    path('like', views.LikeView.as_view(), name='like'),
    path('share', views.ShareView.as_view(), name='share'),
    path('score', views.ScoreView.as_view(), name='score'),
    path('score/average', views.ScoreAverageView.as_view(), name='score_average'),

    # i should delete this i think
    # path("follow/followw/", FollowListsView.as_view(), name="followw"),

    path("follow/followers/", FollowersListView.as_view(), name="followers-list"),
    path("follow/followings/", FollowingsListView.as_view(), name="followings-list"),

    path("like/likers/", LikersListView.as_view(), name="likers-list"),
    path("like/likees/", LikeesListView.as_view(), name="likees-list"),

    
    path("like/dislikers/", DislikersListView.as_view(), name="dislikers-list"),
    path("like/dislikees/", DislikeesListView.as_view(), name="dislikees-list"),

]

