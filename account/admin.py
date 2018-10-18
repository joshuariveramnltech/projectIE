from django.contrib import admin
from .forms import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import (
    StudentProfile, FacultyProfile,
    StaffProfile, Year, YearAndSection
)

# Register your models here.
User = get_user_model()

admin.site.unregister(Group)

admin.site.register(User, UserAdmin)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'course_description', 'year_and_section', 'status']
    search_fields = ['user__email', 'course', 'status', 'user__username']
    list_filter = ['status', 'course', 'year_and_section']


@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ['user', ]
    search_fields = ['user__email', 'user__username']
    list_filter = ['status', 'is_chairperson', 'civil_status']


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', ]
    search_fields = ['user__email', 'user__username']


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ['course', 'year']
    search_fields = ['course', 'year']
    list_filter = ['course', 'year']


@admin.register(YearAndSection)
class YearAndSectionAdmin(admin.ModelAdmin):
    list_display = ['year', 'section']
    search_fields = ['year__year', 'year__course', 'section']
    list_filter = ['section', 'year']
