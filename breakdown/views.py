from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import UserSerializer, SurveySerializer
from .models import Survey

from DB.db_manager import db


# Create your views here
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class Survey(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_list_of_surveys(self, request):
        surveys = db.get_projects()

        print("surveys", surveys)
        serializer = SurveySerializer(surveys, many=True)
        print("itself", serializer)
        print("data", serializer.data)
        print("doneeeeeeeeeer")

        res = JsonResponse({"data": serializer.data})
        return res

    def post(self, request):
        Survey.objects.create()
        return Response(status=201)


class Course(APIView):
    """Комнаты чата"""
    permission_classes = [permissions.IsAuthenticated, ]


survey = Survey()
course = Course()
