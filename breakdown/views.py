from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import UserSerializer, SurveySerializer
from .models import Survey


# Create your views here
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class Survey(APIView):
    """Комнаты чата"""
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        surveys = Survey.objects.filter(Q(id=request.id))
        serializer = SurveySerializer(surveys, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        Survey.objects.create()
        return Response(status=201)
