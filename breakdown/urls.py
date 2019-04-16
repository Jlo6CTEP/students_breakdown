from django.urls import path
from breakdown.views import survey, course, authentication, sign_in, test
from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetView, PasswordResetCompleteView


urlpatterns = [
    path('user/surveys', survey.get_list_of_surveys),
    path('users/authenticate', sign_in),
    # path('users/authenticate', LoginView.as_view(redirect_field_name='register'), name='login'),

    # path('login', sign_in)
]
