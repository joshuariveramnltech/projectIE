from django.contrib import admin
from .models import (
    SubjectInstance, SubjectGrade,
    GeneralSubject, SemesterFinalGrade
)


# Register your models here.

@admin.register(GeneralSubject)
class GeneralSubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_code', 'description', 'units']
    search_fields = ['subject_code', 'description']
    list_filter = ['subject_code', 'units']


@admin.register(SubjectInstance)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject', 'semester', 'school_year',
                    'year_and_section', 'instructor', 'schedule']
    search_fields = ['subject__subject_code',
                     'subject__description', 'instructor', 'school_year']
    list_filter = ['year_and_section__year',
                   'year_and_section__section', 'school_year']


@admin.register(SubjectGrade)
class SubjectGradeAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'subject_instance', 'semester', 'final_grade', 'grade_status'
    ]
    search_fields = ['subject_instance__subject__subject_code', 'subject_instance__subject__description',
                     'student__user__email', 'student__user__username', 'semester', 'grade_status'
                     ]
    list_filter = ['semester', 'school_year', 'grade_status']


@admin.register(SemesterFinalGrade)
class SemesterGradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'school_year', 'grade']
    search_fields = ['student__email',
                     'student__username', 'semester', 'school_year']
    list_filter = ['semester', 'school_year']
