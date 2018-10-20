from django.db import models
from datetime import datetime
from account.models import SEMESTER_CHOICES
from django.contrib.auth import get_user_model
from account.models import StudentProfile, FacultyProfile, YearAndSection
from django.dispatch import receiver
from django.db.models.signals import post_save
import re

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
        GeneralSubject, related_name='subject_instance', on_delete=models.SET_NULL, null=True, verbose_name=u'Subject'
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
        unique_together = ('subject', 'instructor', 'school_year', 'year_and_section', 'semester')

    def __str__(self):
        return "{} {} {}".format(
            str(self.subject), str(self.semester),
            str(self.school_year)
        )


class SubjectGrade(models.Model):
    student = models.ForeignKey(StudentProfile, related_name='student_grade', on_delete=models.CASCADE)
    subject_instance = models.ForeignKey(SubjectInstance, related_name='subject_grade', on_delete=models.SET_NULL,
                                         verbose_name=u'Subject', null=True, blank=True)
    semester = models.CharField(max_length=25, choices=SEMESTER_CHOICES, default='First Semester')
    school_year = models.CharField(max_length=15, choices=SY,
                                   default=str(datetime.now().year) + "-" + str(datetime.now().year + 1))
    final_grade = models.CharField(max_length=15, choices=GRADE_CHOICES, blank=True)
    grade_status = models.CharField(max_length=10, editable=False, blank=True)
    is_finalized = models.BooleanField(default=False, verbose_name=u'Finalized?',
                                       help_text='Once finalized, you can no longer make any more changes.')
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Subject Grades'
        unique_together = ('student', 'subject_instance', 'semester', 'school_year')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        possible_choices = ('W', 'INC', 'NOT S', 'D', 'P')
        if self.final_grade:
            __grade = self.final_grade
            if __grade == '5.00' or __grade == '4.00':
                self.grade_status = 'F'
            elif __grade in possible_choices:
                self.grade_status = __grade
            else:
                self.grade_status = 'P'
        else:
            self.grade_status = ''
        super(SubjectGrade, self).save()

    def __str__(self):
        return self.student.user.get_full_name + " " + str(self.subject_instance)


class SemesterFinalGrade(models.Model):
    student = models.ForeignKey(StudentProfile, related_name='semester_grade',
                                on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.CharField(max_length=25, choices=SEMESTER_CHOICES, default='First Semester')
    subject_grades = models.ManyToManyField(SubjectGrade, related_name='semester_subject_grades', symmetrical=False)
    grade = models.CharField(max_length=10, blank=True, default='')
    school_year = models.CharField(max_length=25, choices=SY,
                                   default=str(datetime.now().year) + "-" + str(datetime.now().year + 1))
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.user.get_full_name + " " + self.semester + " " + self.school_year

    class Meta:
        verbose_name_plural = 'Semester Final Grade'
        unique_together = ('student', 'semester', 'school_year')


@receiver(post_save, sender=SubjectGrade)
def add_to_semester_grade(sender, **kwargs):
    semester_final_grade, created = SemesterFinalGrade.objects.get_or_create(
        student=kwargs['instance'].student,
        semester=kwargs['instance'].semester,
        school_year=kwargs['instance'].school_year
    )  # returns a tuple (the object, boolean flag)
    if kwargs['created']:
        if created:
            semester_final_grade = SemesterFinalGrade.objects.get(
                student=kwargs['instance'].student,
                semester=kwargs['instance'].semester,
                school_year=kwargs['instance'].school_year)
        semester_final_grade.subject_grades.add(kwargs['instance'])
        kwargs['instance'].save()


def compute(semester_grade_instance):
    total_units = 0
    pattern = r'^NSTP|PHED'
    for subject_grade in semester_grade_instance.subject_grades.all():
        if subject_grade.final_grade not in (
                'P', 'W', 'D',
                'NOT S', 'INC', ''
        )and not re.search(pattern, subject_grade.subject_instance.subject.subject_code):
            total_units = total_units + subject_grade.subject_instance.subject.units
    if not total_units:
        return ''
    raw_sum = 0.0
    for subject_grade in semester_grade_instance.subject_grades.all():
        try:
            if not re.search(pattern, subject_grade.subject_instance.subject.subject_code):
                raw_sum = raw_sum + (float(subject_grade.final_grade) * subject_grade.subject_instance.subject.units)
        except ValueError:
            continue
    result = str(round(raw_sum / total_units, 2))
    return result


@receiver(post_save, sender=SemesterFinalGrade)
def compute_gpa(sender, **kwargs):
    if kwargs['instance'].grade != compute(kwargs['instance']):
        kwargs['instance'].grade = compute(kwargs['instance'])
        kwargs['instance'].save()
