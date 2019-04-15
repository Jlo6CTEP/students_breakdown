from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import UserSerializer, SurveySerializer
from .models import Survey

import json
from django.core.serializers.json import DjangoJSONEncoder

from DB.db_manager import db


"""class Authentication(APIView):
    def login(self, request):
        print("!!!", request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                print("Error. Disabled account")
        else:
            print("invalid login")"""


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

        serializer = SurveySerializer(surveys, many=True)
        json_string = serializer.data

        """
        for survey in surveys:
           survey["due_date"] = str(survey["due_date"])
        surveys = [surveys[0]]
        json_string = json.dumps(
            surveys,
            sort_keys=True,
            indent=1,
            cls=DjangoJSONEncoder
        )
        print(json_string)"""
        res = JsonResponse({"data": json_string})
        return res

    def post(self, request):
        Survey.objects.create()
        return Response(status=201)


class Course(APIView):
    """Комнаты чата"""
    permission_classes = [permissions.IsAuthenticated, ]


survey = Survey()
course = Course()
# authentication = Authentication()
