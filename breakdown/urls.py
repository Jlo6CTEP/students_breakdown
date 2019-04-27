from django.urls import path
from breakdown.views import survey_view, user_view


urlpatterns = [
    path('user/surveys/<int:user_id>', survey_view.get_list_of_surveys),
    path('user/surveys', survey_view.get_list_of_surveys),
    path('surveys/create/<int:user_id>', survey_view.create_survey),
    path('surveys/<user_id>/<survey_id>', survey_view.manage_survey),

    path('users/authenticate', user_view.login),
    path('users/register', user_view.register),
    path('account', user_view.account),

    path('users', user_view.UserList.as_view()),
    path('users/<int:pk>', user_view.UserDetail.as_view()),
]
