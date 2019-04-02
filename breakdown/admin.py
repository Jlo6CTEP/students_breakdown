from django.contrib import admin
from django.contrib.auth.models import User
from .models import Survey


# Register your models here.
#class UserAdmin(admin.ModelAdmin):
#    list_display = ("id", "name", "surname", "username")


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'opened', 'created', 'name',
                    'form_factor', 'min_people', 'max_people')


admin.site.register(Survey, SurveyAdmin)
