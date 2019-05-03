from django.contrib import admin
from .models import *


class SurveyAdmin(admin.ModelAdmin):
    list_filter = ('course_id', 'is_formed', 'due_date')
    list_display = (
        'survey_id', 'survey_name',
        'is_formed',
        'due_date',
        'course_id',
        'min_student', 'max_student',
        'group_by',
        'description',
        'additional_info'
    )


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'name')

'''
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language_id', 'language')
    # list_display_links =
'''

class PollAdmin(admin.ModelAdmin):
    list_display = ('poll_id',
                    'topic1', 'topic2', 'topic3',
                    'user_id', 'course_id', 'survey_id',
                    'language1', 'language2', 'language3',
                    'group_by',)


class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'group')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'topic_id', 'course_id')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic_id', 'topic_name', 'description', 'additional_info')


admin.site.register(Poll, PollAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Course, CourseAdmin)
# admin.site.register(Language, LanguageAdmin)
admin.site.register(StudyGroup, StudyGroupAdmin)

