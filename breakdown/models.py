from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "breakdown_course"
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Survey(models.Model):
    GROUP_BY_CHOICES = [(3, "Group"), (2, "Course"), (1, "TA")]

    survey_id = models.AutoField(primary_key=True)
    survey_name = models.CharField(max_length=20)
    is_formed = models.BooleanField(default=True)
    due_date = models.DateTimeField()
    course = models.CharField(max_length=64, null=True)
    course_id = models.IntegerField()
    min_student = models.PositiveIntegerField(default=4)
    max_student = models.PositiveIntegerField(default=6)
    group_by = models.IntegerField(choices=GROUP_BY_CHOICES)
    description = models.CharField(max_length=128)
    additional_info = models.CharField(max_length=512)

    def __str__(self):
        return str(self.survey_id) + ". " + self.survey_name + " [" + str(self.course_id) + "]"

    class Meta:
        db_table = "survey"
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"


'''
class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=128)

    class Meta:
        db_table = "language"
        verbose_name = "Language"
        verbose_name_plural = "Languages"'''''


class Poll(models.Model):
    poll_id = models.AutoField(primary_key=True)
    topic1 = models.IntegerField()
    topic2 = models.IntegerField()
    topic3 = models.IntegerField()
    user_id = models.IntegerField()
    course_id = models.IntegerField()
    survey_id = models.IntegerField()
    #  language1 = models.IntegerField()
    # language2 = models.IntegerField()
    # language3 = models.IntegerField()
    group_by = models.IntegerField()

    class Meta:
        db_table = "poll"
        verbose_name = "Poll"
        verbose_name_plural = "Polls"


class StudyGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    group = models.CharField(max_length=20)

    class Meta:
        db_table = "study_group"
        verbose_name = "Study Group"
        verbose_name_plural = "Study Groups"


class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    additional_info = models.CharField(max_length=512)

    class Meta:
        db_table = "topic"
        verbose_name = "Topic"
        verbose_name_plural = "Topics"


class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    topic_id = models.IntegerField()
    course_id = models.IntegerField()

    class Meta:
        db_table = "team"
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class CourseList(models.Model):
    user_id = models.IntegerField()
    course_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "course_list"
        verbose_name = "Course list"
        verbose_name_plural = "Course lists"


class GroupBy(models.Model):
    grouping_id = models.IntegerField(primary_key=True)
    group_by = models.CharField(max_length=20)

    class Meta:
        db_table = "group_by"
        verbose_name = "Group by"
        verbose_name_plural = "Group by"


class GroupSurveyList(models.Model):
    survey_id = models.IntegerField()
    group_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "group_survey_list"
        verbose_name = "Group survey list"
        verbose_name_plural = "Group survey lists"


class StudentTeamList(models.Model):
    user_id = models.IntegerField()
    team_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "student_team_list"
        verbose_name = "Student team list"
        verbose_name_plural = "Student team lists"


class SurveyTopicList(models.Model):
    topic_id = models.IntegerField()
    survey_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "survey_topic_list"
        verbose_name = "Survey topic list"
        verbose_name_plural = "Survey topic lists"


class TaSurveyList(models.Model):
    user_id = models.IntegerField()
    survey_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "ta_survey_list"
        verbose_name = "TA survey list"
        verbose_name_plural = "TA Survey lists"


class UserGroupList(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "user_group_list"
        verbose_name = "User group list"
        verbose_name_plural = "User group lists"


class UserTopicList(models.Model):
    user_id = models.IntegerField()
    topic_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "user_topic_list"
        verbose_name = "User topic list"
        verbose_name_plural = "User topic lists"
