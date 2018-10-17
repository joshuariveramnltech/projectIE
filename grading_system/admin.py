from django.contrib import admin
from .models import Subject, SubjectGrade


# Register your models here.

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_code', 'description']


@admin.register(SubjectGrade)
class SubjectGradeAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'subject', 'instructor', 'grade'
    ]
