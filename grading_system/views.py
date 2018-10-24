from django.shortcuts import render, reverse
from .models import SubjectInstance, SubjectGrade
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from .models import SemesterFinalGrade
from .forms import UpdateSubjectGrade
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
import weasyprint
from django.conf import settings
# Create your views here.

User = get_user_model()


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
    if latest_semester_grade:  # checks if there's a result in the prior query
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
    current = SubjectInstance.objects.all().values(
        'school_year', 'semester').distinct().order_by('-semester', '-school_year').first()
    subject_list = SubjectInstance.objects.filter(
        year_and_section=request.user.student_profile.year_and_section,
        school_year=current['school_year'],
        semester=current['semester']
    ).order_by('-semester')
    enrolled_subjects = SubjectGrade.objects.filter(
        student=request.user.student_profile,
        school_year=current['school_year'],
        semester=current['semester']
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
                    ) # retrive semester final grade instance
                except SemesterFinalGrade.DoesNotExist:
                    SemesterFinalGrade.objects.create(
                        student=request.user.student_profile,
                        semester=subject.semester,
                        school_year=subject.school_year,
                    ) # create semester final grade instance
                    semester_grade = SemesterFinalGrade.objects.get(
                        student=request.user.student_profile,
                        semester=subject.semester,
                        school_year=subject.school_year,
                    ) # retrieve semester grade instance
                semester_grade.subject_grades.add(subject_grade)
            return HttpResponseRedirect(reverse('grading_system:student_registration'))
    context = {'subject_list': subject_list,
               'enrolled_subjects': enrolled_subjects,
               'current_semester' : current['semester'],
               'current_school_year': current['school_year']}
    return render(request, 'student_registration.html', context)


# for chairperson only
@login_required
def view_all_students_chairperson(request):
    if not request.user.faculty_profile.is_chairperson:
        raise PermissionDenied
    student_list = User.objects.filter(
        is_student=True, ).order_by('-date_joined')
    if request.user.faculty_profile.department == "Department of Industrial Engineering":
        student_list = student_list.filter(student_profile__course='BSIE')
    student_query = request.GET.get('student_query')
    if student_query:
        student_list = student_list.filter(
            Q(first_name__icontains=student_query) |
            Q(last_name__icontains=student_query) |
            Q(username__icontains=student_query) |
            Q(email__icontains=student_query)
        ).distinct()
    student_paginator = Paginator(student_list, 20)
    student_page = request.GET.get('student_page')
    try:
        students = student_paginator.page(student_page)
    except PageNotAnInteger:
        students = student_paginator.page(1)
    except EmptyPage:
        students = student_paginator.page(student_paginator.num_pages)
    context = {'students': students}
    return render(request, 'view_all_students_chairperson.html', context)


# chairperson only
@login_required
def student_tagging(request, student_id, student_username):
    if not request.user.faculty_profile.is_chairperson:
        raise PermissionDenied
    student = User.objects.get(id=student_id)
    current = SubjectInstance.objects.all().values(
        'school_year', 'semester').distinct().order_by('-semester', '-school_year').first()
    student_subject_list = SubjectGrade.objects.filter(
        student=student.student_profile).order_by('-semester', '-school_year', '-date_created')
    subject_list = SubjectInstance.objects.filter(
        school_year=current['school_year'],
        semester=current['semester']
    ).order_by('-date_created')
    subject_query = request.GET.get('subject_query')
    record_query = request.GET.get('record_query')
    if subject_query:
        subject_list = subject_list.filter(
            Q(subject__subject_code__icontains=subject_query) |
            Q(subject__description__icontains=subject_query) |
            Q(school_year__icontains=subject_query) |
            Q(semester__icontains=subject_query)
        ).distinct()
    if record_query:
        student_subject_list = student_subject_list.filter(
            Q(subject_instance__subject__subject_code__icontains=record_query) |
            Q(subject_instance__subject__description__icontains=record_query) |
            Q(subject_instance__school_year__icontains=record_query) |
            Q(subject_instance__semester__icontains=record_query)
        ).distinct()
    subject_paginator = Paginator(subject_list, 10)
    subject_page = request.GET.get('subject_page')
    try:
        subjects = subject_paginator.page(subject_page)
    except PageNotAnInteger:
        subjects = subject_paginator.page(1)
    except EmptyPage:
        subjects = subject_paginator.page(subject_paginator.num_pages)
    student_subject_paginator = Paginator(student_subject_list, 10)
    student_subject_page = request.GET.get('student_subject_page')
    try:
        student_subjects = student_subject_paginator.page(student_subject_page)
    except PageNotAnInteger:
        student_subjects = student_subject_paginator.page(1)
    except EmptyPage:
        student_subjects = student_subject_paginator.page(
            student_subject_paginator.num_pages)
    if request.method == "POST":
        sub_list = request.POST.getlist('selected_subjects')
        for each in sub_list:
            subject = SubjectInstance.objects.get(id=int(each))
            SubjectGrade.objects.create(
                student=student.student_profile,
                subject_instance=subject,
                semester=subject.semester,
                school_year=subject.school_year,
            )  # create subject grade instance
            subject_grade = SubjectGrade.objects.get(
                student=student.student_profile,
                subject_instance=subject,
                semester=subject.semester,
                school_year=subject.school_year,
            )  # retrieve created subject grade instance
            try:
                semester_grade = SemesterFinalGrade.objects.get(
                    student=student.student_profile,
                    semester=subject.semester,
                    school_year=subject.school_year,
                )
            except SemesterFinalGrade.DoesNotExist:
                SemesterFinalGrade.objects.create(
                    student=student.student_profile,
                    semester=subject.semester,
                    school_year=subject.school_year,
                )
                semester_grade = SemesterFinalGrade.objects.get(
                    student=student.student_profile,
                    semester=subject.semester,
                    school_year=subject.school_year,
                )
            semester_grade.subject_grades.add(subject_grade)
        return HttpResponseRedirect(reverse('grading_system:student_tagging', args=[student_id, student_username]))
    context = {'student': student, 'subjects': subjects,
               'student_subjects': student_subjects}
    return render(request, 'student_tagging.html', context)


# for chairperson only
@login_required
def remove_subject_chairperson(request, subject_grade_id, student_id, student_username):
    if not request.user.faculty_profile.is_chairperson:
        raise PermissionDenied
    instance = SubjectGrade.objects.get(id=subject_grade_id)
    instance.delete()
    return HttpResponseRedirect(reverse('grading_system:student_tagging', args=[student_id, student_username]))


# for faculty only
@login_required
def class_list_pdf(request, subject_instance_id, subject_code):
    if not request.user.is_faculty:
        raise PermissionDenied
    current_date_time = str(datetime.now().strftime('%h %d %Y %H:%M'))
    subject_instance = SubjectInstance.objects.get(id=subject_instance_id)
    protocol = request.build_absolute_uri().split(':')[0]
    subject_students = User.objects.filter(
        student_profile__student_grade__subject_instance=subject_instance)
    context = {
        'subject_instance': subject_instance,
        'protocol': protocol,
        'subject_students': subject_students,
        'current_date_time': current_date_time
    }
    html = render_to_string('class_list_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response["Content-Disposition"] = "filename='class_list{}_{}.pdf'".format(
        subject_instance.subject.description, subject_instance.year_and_section)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(settings.STATIC_ROOT + '/main.css'), ])
    return response


# for faculty only
@login_required
def print_schedule_pdf(request):
    if not request.user.is_faculty:
        raise PermissionDenied
    current_date_time = str(datetime.now().strftime('%h %d %Y %H:%M'))
    current = SubjectInstance.objects.all().values(
        'school_year', 'semester').distinct().order_by('-semester', '-school_year').first()
    assigned_subjects_per_year = SubjectInstance.objects.filter(
        instructor=request.user.faculty_profile,
        school_year=current['school_year'],
        semester=current['semester']
    ).order_by('-semester', '-date_created')
    context = {'assigned_subjects_per_year': assigned_subjects_per_year,
               'current_date_time': current_date_time, 'current_school_year': current['school_year']}
    html = render_to_string('print_schedule_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "filename='schedule_{}.pdf'".format(
        current['school_year'])
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(settings.STATIC_ROOT + '/main.css'), ])
    return response
