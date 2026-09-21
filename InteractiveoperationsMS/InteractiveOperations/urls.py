# InteractiveOperations/urls.py
from django.urls import path
from . import views

app_name = 'interactive_operations'

urlpatterns = [
    path('test_api', views.TestApi.as_view(), name='test_api'),
    path('follow', views.FollowView.as_view(), name='follow'),
    path('like', views.LikeView.as_view(), name='like'),
    path('share', views.ShareView.as_view(), name='share'),
    path('score', views.ScoreView.as_view(), name='score'),
    path('score/average', views.ScoreAverageView.as_view(), name='score_average'),

    path("follow/followers", views.FollowersListView.as_view(), name="followers-list"),
    path("follow/followings", views.FollowingsListView.as_view(), name="followings-list"),

    path("like/likers", views.LikersListView.as_view(), name="likers-list"),
    path("like/likees", views.LikeesListView.as_view(), name="likees-list"),

    path("like/dislikers", views.DislikersListView.as_view(), name="dislikers-list"),
    path("like/dislikees", views.DislikeesListView.as_view(), name="dislikees-list")
]