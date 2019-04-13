from django.urls import path
from . import views

urlpatterns = [
    path('', views.names),
    path('user/surveys', views.surveys)
  
]
