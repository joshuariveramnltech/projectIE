from django.db import models
from datetime import datetime
from account.models import SEMESTER_CHOICES
from django.contrib.auth import get_user_model
from account.models import StudentProfile, FacultyProfile, YearAndSection

# Create your models here.

User = get_user_model()

SY = []

for year in range(2010, datetime.now().year + 15):
    SY.append(
        (
            str(year) + "-" + str(year + 1), str(year) + "-" + str(year + 1)
        )
    )

GRADE_CHOICES = (
    ('1.00', '1.00'), ('1.25', '1.25'),
    ('1.50', '1.50'), ('1.75', '1.75'),
    ('2.00', '2.00'), ('2.25', '2.25'),
    ('2.50', '2.50'), ('2.75', '2.75'),
    ('3.00', '3.00'), ('4.00', '4.00'),
    ('5.00', '5.00'), ('P', 'P'),
    ('D', 'D'), ('INC', 'INC'),
    ('W', 'W'), ('NOT S', 'NOT S')
)


class Subject(models.Model):
    subject_code = models.CharField(max_length=50)
    description = models.CharField(max_length=75)
    semester = models.CharField(max_length=25, choices=SEMESTER_CHOICES, default='First Semester')
    year_and_section = models.ForeignKey(YearAndSection, related_name='subjects', on_delete=models.DO_NOTHING)
    school_year = models.CharField(max_length=15, choices=SY)
    units = models.PositiveSmallIntegerField()
    prerequisite = models.CharField(max_length=25, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            'subject_code', 'description', 'school_year', 'year_and_section'
        )

    def __str__(self):
        return self.subject_code + " " + self.description


class SubjectGrade(models.Model):
    student = models.ForeignKey(StudentProfile, related_name='student_grade', on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, related_name='subject_grade', on_delete=models.DO_NOTHING)
    instructor = models.ForeignKey(FacultyProfile, related_name='given_grade', on_delete=models.DO_NOTHING)
    grade = models.CharField(max_length=15, choices=GRADE_CHOICES, default='1.00')
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Subject Grades'
        unique_together = ('student', 'subject')

    def __str__(self):
        return self.student.user.get_full_name + " " + str(self.subject)
