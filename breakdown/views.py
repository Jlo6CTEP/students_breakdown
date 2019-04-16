from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

import json

from .models import Survey
from .serializers import UserSerializer, SurveySerializer


from DB.db_manager import db


def test(request):
    print(request.method)
    return sign_in(request)


# @csrf_exempt
@api_view(['GET', 'POST', ])
@permission_classes((permissions.AllowAny,))
def sign_in(request):
    print("qwe")
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
            res = JsonResponse({"data": "1"})
            return Response("Success", status=HTTP_STATUS_OK)
        else:
            print("Error. Disabled account")
            return Response("Disabled account", status=410)
    else:
        print("invalid login")
        return Response("Invalid login", status=400)
    return Response(status=HTTP_STATUS_OK)


class Authentication(APIView):
    pass




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
authentication = Authentication()
