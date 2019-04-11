from django.db.models import Q
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import UserSerializer, ProjectSerializer
from .models import Project


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
        surveys = Project.objects.filter(Q(id=request.id))
        serializer = ProjectSerializer(surveys, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        Project.objects.create()
        return Response(status=201)


class Course(APIView):
    """Комнаты чата"""
    permission_classes = [permissions.IsAuthenticated, ]
