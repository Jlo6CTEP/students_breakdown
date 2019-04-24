from django.urls import path
from breakdown.views import survey, login, account, register,\
    logout, UserList, UserDetail


urlpatterns = [
    path('user/surveys/<int:user_id>', survey.get_list_of_surveys),
    path('user/surveys', survey.get_list_of_surveys),

    path('users/authenticate', login),
    path('users/register', register),
    path('account', account),

    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]
