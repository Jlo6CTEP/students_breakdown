from django.urls import path
from breakdown.views import survey, login, logout, UserList, UserDetail


urlpatterns = [
    path('user/surveys', survey.get_list_of_surveys),
    path('users/authenticate', login),

    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]
