from django.shortcuts import render
from .models import SubjectInstance
# from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import SemesterFinalGrade


# Create your views here.


@login_required
def test(request):
    if not request.user.is_student:
        raise PermissionDenied
    subjects = SubjectInstance.objects.filter(
        year_and_section=request.user.student_profile.year_and_section
    ).values_list('year_and_section', flat=True).distinct()
    context = {'request': request, 'subjects': subjects}
    return render(request, 'test.html', context)


@login_required
def view_all_grades(request):
    if not request.user.is_student:
        raise PermissionDenied
    grades = SemesterFinalGrade.objects.filter(
        student=request.user.student_profile
    ).order_by('-school_year', '-semester', '-date_created')
    context = {'request': request, 'grades': grades}
    return render(request, 'view_all_grades.html', context)
