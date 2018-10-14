from django.contrib import admin
from .forms import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import StudentProfile, FacultyProfile, StaffProfile

# Register your models here.
User = get_user_model()

admin.site.unregister(Group)

admin.site.register(User, UserAdmin)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', ]


@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ['user', ]


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', ]
