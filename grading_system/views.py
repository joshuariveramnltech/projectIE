from django.shortcuts import render, reverse
from .models import SubjectInstance, SubjectGrade
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from .models import SemesterFinalGrade
from .forms import UpdateSubjectGrade
from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import datetime

# Create your views here.


# student only
@login_required
def view_all_grades(request):
    if not request.user.is_student:
        raise PermissionDenied
    grades = SemesterFinalGrade.objects.filter(
        student=request.user.student_profile
    ).order_by('-school_year', '-semester', '-date_created')
    context = {'grades': grades}
    return render(request, 'view_all_grades.html', context)


# student only
@login_required
def view_schedule_student(request):
    if not request.user.is_student:
        raise PermissionDenied
    latest_semester_grade = SemesterFinalGrade.objects.all().order_by(
        '-school_year',
        '-semester',
        '-date_created'
    ).first()
    latest_semester_grade = latest_semester_grade.subject_grades.all()
    context = {'latest_semester_grade': latest_semester_grade}
    return render(request, 'view_schedule_student.html', context)


# faculty view
@login_required
def view_assigned_subjects(request):
    if not request.user.is_faculty:
        raise PermissionDenied
    context = {}
    assigned_subject_list = SubjectInstance.objects.filter(
        instructor=request.user.faculty_profile).order_by('-date_created')
    assigned_subject_query = request.GET.get('assigned_subject_query')
    if assigned_subject_query:
        assigned_subject_list = assigned_subject_list.filter(
            Q(subject__subject_code__icontains=assigned_subject_query) |
            Q(subject__description__icontains=assigned_subject_query) |
            Q(school_year__icontains=assigned_subject_query)
        ).distinct()
    assigned_subject_paginator = Paginator(assigned_subject_list, 10)
    assigned_subject_page = request.GET.get('assigned_subject_page')
    try:
        assigned_subjects = assigned_subject_paginator.page(
            assigned_subject_page)
    except PageNotAnInteger:
        assigned_subjects = assigned_subject_paginator.page(1)
    except EmptyPage:
        assigned_subjects = assigned_subject_paginator.page(
            assigned_subject_paginator.num_pages)

    context['assigned_subjects'] = assigned_subjects
    return render(request, 'view_assigned_subjects.html', context)


# for faculty only
@login_required
def view_students_per_subject(request, subject_instance_id, subject_code):
    if not request.user.is_faculty:
        raise PermissionDenied
    context = {}
    subject_instance = SubjectInstance.objects.get(id=subject_instance_id)
    subject_grades = SubjectGrade.objects.filter(
        subject_instance=subject_instance)
    context.update({'subject_grades': subject_grades,
                    'subject_instance': subject_instance})
    return render(request, 'view_students_per_subject.html', context)


# for faculty only
@login_required
def view_update_grade(request, subject_grade_id):
    if not request.user.is_faculty:
        raise PermissionDenied
    subject_grade = SubjectGrade.objects.get(id=subject_grade_id)
    if subject_grade.is_finalized:
        return render(request, 'request_error.html', {})
    if request.method == 'GET':
        update_subject_grade_form = UpdateSubjectGrade(instance=subject_grade)
    elif request.method == 'POST':
        update_subject_grade_form = UpdateSubjectGrade(
            instance=subject_grade, data=request.POST)
        if update_subject_grade_form.is_valid():
            instance = update_subject_grade_form.save(commit=False)
            update_subject_grade_form.save()
            messages.success(request, 'Grade Updated Successfully')
            if instance.is_finalized:
                return HttpResponseRedirect(
                    reverse(
                        'grading_system:view_students_per_subject',
                        args=[subject_grade.subject_instance.id,
                              subject_grade.subject_instance.subject.subject_code]
                    )
                )
            return HttpResponseRedirect(reverse('grading_system:view_update_grade', args=[subject_grade_id, ]))
    context = {'subject_grade': subject_grade,
               'update_subject_grade_form': update_subject_grade_form
               }
    return render(request, 'view_update_grade.html', context)


# student only
@login_required
def student_registration(request):
    if not request.user.is_student:
        raise PermissionDenied
    subject_list = SubjectInstance.objects.filter(
        year_and_section=request.user.student_profile.year_and_section,
        school_year=str(datetime.now().year) + "-" +
        str(datetime.now().year+1)
    ).order_by('-semester')
    enrolled_subjects = SubjectGrade.objects.filter(
        student=request.user.student_profile,
        school_year=str(datetime.now().year) + "-" +
        str(datetime.now().year+1)
    ).order_by('-subject_instance__semester')
    if request.method == "POST":
        selected_subjects = request.POST.getlist('selected_subjects')
        if selected_subjects:
            for each in selected_subjects:
                subject = SubjectInstance.objects.get(id=int(each))
                SubjectGrade.objects.create(
                    student=request.user.student_profile,
                    subject_instance=subject,
                    semester=subject.semester,
                    school_year=subject.school_year,
                )  # create subject grade instance
                subject_grade = SubjectGrade.objects.get(
                    student=request.user.student_profile,
                    subject_instance=subject,
                    semester=subject.semester,
                    school_year=subject.school_year,
                )  # retrieve created subject grade instance
                try:
                    semester_grade = SemesterFinalGrade.objects.get(
                        student=request.user.student_profile,
                        semester=subject.semester,
                        school_year=subject.school_year,
                    )
                except SemesterFinalGrade.DoesNotExist:
                    semester_grade = SemesterFinalGrade.objects.create(
                        student=request.user.student_profile,
                        semester=subject.semester,
                        school_year=subject.school_year,
                    )
                    semester_grade = SemesterFinalGrade.objects.get(
                        student=request.user.student_profile,
                        semester=subject.semester,
                        school_year=subject.school_year,
                    )
                semester_grade.subject_grades.add(subject_grade)
            return HttpResponseRedirect(reverse('grading_system:student_registration'))
    context = {'subject_list': subject_list,
               'enrolled_subjects': enrolled_subjects}
    return render(request, 'student_registration.html', context)


# for chairperson only
@login_required
def assigned_faculty_to_subject(request):
    if not request.user.faculty_profile.is_chairperson:
        raise PermissionDenied
    context = {}
    return render(request, 'assigned_faculty_to_subject.html', context)
