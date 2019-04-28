from rest_framework import serializers
from django.contrib.auth.models import User
from breakdown.models import Survey, Course


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", 'first_name', 'last_name')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('course_id', 'name')


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = (
            'survey_id', 'survey_name', 'due_date',
            'course', 'min_student', 'max_student', 'is_formed',
            'group_by', 'description', 'additional_info'
        )



