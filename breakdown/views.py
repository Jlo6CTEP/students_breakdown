from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.request import HttpRequest

from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .serializers import UserSerializer


from DB.db_manager import db


import json

from .models import Survey
from .serializers import UserSerializer, SurveySerializer


from DB.db_manager import db


@api_view(['GET', 'POST', ])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((permissions.AllowAny,))
def login(request):
    print("Entered to sign in view")
    print(request.body)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    username = body['username']
    password = body['password']

    print(username, password)

    user = authenticate(username=username, password=password)
    print("authenticated")
    if user is not None:
        if user.is_active:
            # messages.success(request._request, "Success")
            login(request, user)
            res = db.check_credentials(username, password)
            print(res)
            token = Token.objects.create(user=res["id"])
            print(token)
            # res["token"] = token
            return JsonResponse(res, status=200)
        else:
            print("Error. Disabled account")
            return Response("Disabled account", status=410)
    else:
        print("Error. Invalid login")
        return Response("Invalid login", status=400)


@api_view(['GET', 'POST', ])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((permissions.IsAuthenticated,))
def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return Response(status=400)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class Survey(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_list_of_surveys(self, request):
        surveys = db.get_projects()
        print(surveys)
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
    permission_classes = [permissions.IsAuthenticated, ]


survey = Survey()
course = Course()
