from rest_framework import serializers
from django.contrib.auth.models import User
from breakdown.models import Survey, Course


class UserSerializer(serializers.ModelSerializer):
    surveys = serializers.PrimaryKeyRelatedField(many=True, queryset=Survey.objects.all())

    """Serialization of user"""
    class Meta:
        model = User
        fields = ("id", "username", 'first_name', 'last_name', 'surveys')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('course_id', 'name')


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = (
            'project_id', 'project_name', 'due_date',
            'course', 'min_student', 'max_student', 'is_formed',
            'group_by', 'description', 'additional_info'
        )



