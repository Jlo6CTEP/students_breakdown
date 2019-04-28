from django.contrib import admin
from .models import Survey, Course


class ProjectAdmin(admin.ModelAdmin):
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


admin.site.register(Survey, ProjectAdmin)
admin.site.register(Course, CourseAdmin)
