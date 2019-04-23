import json

from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.db.utils import IntegrityError as DjangoIntegrityError
from django.contrib.auth.forms import UserCreationForm


from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from .models import Survey
from DB.db_manager import db
from .serializers import UserSerializer, SurveySerializer


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


@api_view(['GET', ])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((permissions.IsAuthenticated,))
def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', ])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((permissions.AllowAny,))
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if True or form.is_valid():
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            username = body['username']
            password = body['password']
            first_name = body['firstName']
            last_name = body['lastName']
            try:
                user = User.objects.create_user(username=username,
                                                email=username,
                                                password=password,
                                                first_name=first_name,
                                                last_name=last_name)
            except DjangoIntegrityError:
                return Response("User already exists", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            res = dict(zip(["id", "username"], [user.id, user.get_username()]))
            return JsonResponse(res, status=status.HTTP_200_OK, safe=False)
    else:
        form = UserCreationForm()
        return Response("Method is not POST", status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', ])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def account(request):
    return Response(status=status.HTTP_202_ACCEPTED)


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

    @staticmethod
    def get_list_of_surveys(request):
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

    @staticmethod
    def post(request):
        Survey.objects.create()
        return Response(status=status.HTTP_201_CREATED)


class Course(APIView):
    permission_classes = [permissions.IsAuthenticated, ]


survey = Survey()
course = Course()
