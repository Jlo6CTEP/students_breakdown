import json

from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.db.utils import IntegrityError as DjangoIntegrityError


from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from .models import Survey
from DB.db_manager import db
from .serializers import UserSerializer, SurveySerializer


class UserView:
    class UserList(generics.ListAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer

    class UserDetail(generics.RetrieveAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer

    class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all().order_by('-date_joined')
        serializer_class = UserSerializer

    @staticmethod
    @api_view(['POST', ])
    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((permissions.AllowAny,))
    def login(request):
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        username = body['username']
        password = body['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                django_login(request, user)
                res = db.check_credentials(username, password)
                if not res:
                    return Response("Wrong login or password", status=status.HTTP_400_BAD_REQUEST)
                token, created = Token.objects.get_or_create(user=user)
                res["token"] = token.key
                print(res, token)
                return JsonResponse(res, status=status.HTTP_200_OK)
            else:
                return Response("Inactive account", status=status.HTTP_410_GONE)
        else:
            return Response("Invalid login", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['GET', ])
    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((permissions.IsAuthenticated,))
    def logout(request):
        auth.logout(request)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['POST', ])
    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((permissions.AllowAny,))
    def register(request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body['username']
        password = body['password']
        first_name = body['firstName']
        last_name = body['lastName']
        try:
            user = User.objects.create_user(username=username, password=password,
                                            email=username, first_name=first_name, last_name=last_name)
        except DjangoIntegrityError:
            return Response("User already exists", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        res = dict(zip(["id", "username"], [user.id, user.get_username()]))
        return JsonResponse(res, status=status.HTTP_200_OK, safe=False)

    @staticmethod
    @api_view(['GET', 'POST', ])
    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((permissions.IsAuthenticatedOrReadOnly,))
    def account(request):
        return Response(status=status.HTTP_202_ACCEPTED)


class SurveyView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @staticmethod
    def get_list_of_surveys(request, user_id=None):
        print(user_id)
        surveys = db.get_projects()
        # surveys = db.get_student_projects()
        print(surveys)
        serializer = SurveySerializer(surveys, many=True)
        json_string = serializer.data
        res = JsonResponse({"data": json_string})
        return res

    @staticmethod
    def post(request):
        Survey.objects.create()
        return Response(status=status.HTTP_201_CREATED)


class CourseView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]


survey_view = SurveyView()
course_view = CourseView()
user_view = UserView()
