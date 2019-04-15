from django.urls import path
from breakdown.views import survey, course

urlpatterns = [
    path('user/surveys', survey.get_list_of_surveys)
]
