from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Survey(models.Model):
    FORM_FACTOR_CHOICES = [("GR", "Group"), ("CO", "Course"), ("TA", "TA")]

    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=30)
    opened = models.BooleanField(default=True)
    created = models.DateTimeField()
    name = models.CharField(max_length=30)
    description = models.TextField()
    add_info = models.TextField()
    form_factor = models.CharField(max_length=30, choices=FORM_FACTOR_CHOICES)
    min_people = models.PositiveIntegerField(default=4)
    max_people = models.PositiveIntegerField(default=6)

    def __str__(self):
        return str(self.id) + ". " + self.course + "." + self.name

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
