from django.urls import path
from breakdown.views import survey_view, user_view, team_view


urlpatterns = [
    path('users/authenticate', user_view.login),
    path('users/register', user_view.register),
    path('users', user_view.UserList.as_view()),
    path('users/<int:pk>', user_view.UserDetail.as_view()),
    path('account', user_view.account),  # TODO delete if not necessary

    path('surveys/create', survey_view.create_survey),
    path('surveys/<int:user_id>', survey_view.get_list_of_surveys_by_user_id),
    path('surveys/<int:user_id>/<int:survey_id>', survey_view.manage_survey),
    path('surveys', survey_view.get_list_of_surveys),  # TODO delete if not necessary

    # TODO uncomment to use team_view
    # path('/teams/form/<int:user_id>/<int:survey_id>', team_view.form_teams),
    # path('/teams/<int:user_id>/<int:survey_id}', team_view.get_all_teams),
    # path('/teams/<int:user_id>/<int:survey_id>/<int:team_id>', team_view.manage_team)

]
