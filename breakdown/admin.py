from django.contrib import admin
from .models import Project, Course


class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('course_id', 'is_open')
    list_display = (
        'project_id', 'project_name',
        'is_open',
        'due_date',
        'course_id',
        'min_student', 'max_student',
        'group_by',
        'description',
        'additional_info'
    )


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'name')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Course, CourseAdmin)
