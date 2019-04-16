from django.urls import path
from breakdown.views import survey, course, authentication

urlpatterns = [
    path('user/surveys', survey.get_list_of_surveys),
    path('login', authentication.sign_in)
]
