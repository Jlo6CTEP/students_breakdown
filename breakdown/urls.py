from django.urls import path
from breakdown.views import survey, sign_in, UserList, UserDetail
from django.conf.urls import include
from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetView, PasswordResetCompleteView


urlpatterns = [
    path('user/surveys', survey.get_list_of_surveys),
    path('users/authenticate', sign_in),
    path('accounts/profile/', survey.get_list_of_surveys),
    # path('users/authenticate', LoginView.as_view(redirect_field_name='register'), name='login'),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    # path('login', sign_in)
]
