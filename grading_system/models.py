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

GRADE_STATUS_CHOICES = (('P', 'P'), ('F', 'F'), ('INC', 'INC'),
                        ('D', 'D'), ('W', 'W')
                        )

possible_choices = ('W', 'INC', 'NOT S', 'D')


class GeneralSubject(models.Model):
    subject_code = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=75)
    units = models.PositiveSmallIntegerField()
    prerequisite = models.ManyToManyField('self', symmetrical=False, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Curriculum'
        unique_together = ('subject_code', 'description')

    def __str__(self):
        return self.subject_code + " " + self.description

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if (self.subject_code != self.subject_code.strip().upper() or
                self.description != self.description.strip().title()):
            self.subject_code = self.subject_code.strip().upper()
            self.description = self.description.strip().title()
        super(GeneralSubject, self).save()


class SubjectInstance(models.Model):
    subject = models.ForeignKey(
        GeneralSubject, related_name='subject_instance', on_delete=models.SET_NULL, null=True
    )
    instructor = models.ForeignKey(
        FacultyProfile, related_name='given_grade', on_delete=models.SET_NULL, null=True, blank=True
    )
    school_year = models.CharField(max_length=15, choices=SY,
                                   default=str(datetime.now().year) + "-" + str(datetime.now().year + 1))
    year_and_section = models.ForeignKey(YearAndSection, related_name='subjects', on_delete=models.DO_NOTHING)
    semester = models.CharField(max_length=25, choices=SEMESTER_CHOICES, default='First Semester')
    schedule = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return str(self.subject) + " " + str(self.semester) + " " + str(self.school_year)


class SubjectGrade(models.Model):
    student = models.ForeignKey(StudentProfile, related_name='student_grade', on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectInstance, related_name='subject_grade', on_delete=models.DO_NOTHING)
    school_year = models.CharField(max_length=15, choices=SY,
                                   default=str(datetime.now().year) + "-" + str(datetime.now().year + 1))
    final_grade = models.CharField(max_length=15, choices=GRADE_CHOICES, default='1.00', blank=True)
    grade_status = models.CharField(max_length=15, choices=GRADE_STATUS_CHOICES, editable=False, blank=True)
    is_finalized = models.BooleanField(default=False, verbose_name=u'Finalized?',
                                       help_text='Once finalized, you can no longer make any more changes.')
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Subject Grades'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.final_grade and self.grade_status is None:
            __grade = self.final_grade
            if __grade == '5' or __grade == '4':
                self.grade_status = 'F'
            elif __grade in possible_choices:
                self.grade_status = __grade
            else:
                self.grade_status = 'P'

    def __str__(self):
        return self.student.user.get_full_name + " " + str(self.subject)


class SemesterFinalGrade(models.Model):
    student = models.ForeignKey(StudentProfile, related_name='semester_grade',
                                on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.CharField(max_length=25, choices=SEMESTER_CHOICES, default='First Semester')
    subjects = models.ManyToManyField(SubjectInstance, related_name='semester_subjects', symmetrical=False)
    grade = models.CharField(max_length=10, blank=True, null=True)
    school_year = models.CharField(max_length=25, choices=SY, default='First Semester')
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.user.get_full_name + " " + self.semester + " " + self.school_year

    class Meta:
        verbose_name_plural = 'Semester Final Grade'
        unique_together = ('student', 'semester', 'school_year')
