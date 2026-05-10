from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    # ************************************* get log *******************************************************************

    # ************************************* set database **************************************************************

    # ************************************* Test Token ****************************************************************
    path('actor_test_token/', views.TestToken.as_view(), name='actor_test_token'),

]
