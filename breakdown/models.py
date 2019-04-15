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

    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=20)
    is_open = models.BooleanField(default=True)
    due_date = models.DateTimeField()
    course = models.CharField(max_length=64)
    course_id = models.IntegerField()
    min_student = models.PositiveIntegerField(default=4)
    max_student = models.PositiveIntegerField(default=6)
    group_by = models.IntegerField(choices=GROUP_BY_CHOICES)
    description = models.CharField(max_length=128)
    additional_info = models.CharField(max_length=512)

    def __str__(self):
        return str(self.project_id) + ". " + self.project_name + " [" + str(self.course_id) + "]"

    #@property
    #def course_name(self):
    #    return self.course_id.name

    class Meta:
        db_table = "project"
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"



