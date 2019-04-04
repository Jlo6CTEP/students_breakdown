from rest_framework import serializers
from django.contrib.auth.models import User
from breakdown.models import Project, Course


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("id", "username", 'first_name', 'last_name')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'project_id', 'project_name', 'is_open', 'due_date',
            'course_id', 'min_student', 'max_student',
            'group_by', 'description', 'additional_info'
        )


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('course_id', 'name')
