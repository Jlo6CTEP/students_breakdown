from rest_framework import serializers
from django.contrib.auth.models import User
from breakdown.models import Survey, Course


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("id", "username", 'first_name', 'last_name')


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'course', 'opened', 'created', 'name',
                  'description', 'add_info', 'form_factor', 'min_people', 'max_people')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')
