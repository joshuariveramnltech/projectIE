from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from .forms import PersonalFacultyForm, PersonalStaffForm, PersonalUserForm, PersonalStudentForm

# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {})


@login_required
def change_password(request):
    context = {}
    if request.method == 'GET':
        change_password_form = PasswordChangeForm(user=request.user)
    elif request.method == 'POST':
        change_password_form = PasswordChangeForm(
            user=request.user, data=request.POST)
        if change_password_form.is_valid():
            new_password = change_password_form.save()
            update_session_auth_hash(request, new_password.user)
            messages.success(request, 'Password Change Successful!')
            return HttpResponseRedirect(reverse('account:change_password'))
    context['change_password_form'] = change_password_form
    return render(request, 'change_password.html', context)


@login_required
def view_update_profile(request):
    context = {'request': request}
    personal_profile_form = None
    if request.method == 'GET':
        user_form = PersonalUserForm(instance=request.user)
        if request.user.is_faculty:
            personal_profile_form = PersonalFacultyForm(
                instance=request.user.faculty_profile)
        elif request.user.is_staff:
            personal_profile_form = PersonalStaffForm(
                instance=request.user.staff_profile)
        elif request.user.is_student:
            personal_profile_form = PersonalStudentForm(
                instance=request.user.student_profile)
    elif request.method == 'POST':
        user_form = PersonalUserForm(
            data=request.POST, files=request.FILES, instance=request.user)
        if request.user.is_faculty:
            personal_profile_form = PersonalFacultyForm(
                data=request.POST, instance=request.user.faculty_profile)
        elif request.user.is_staff:
            personal_profile_form = PersonalStaffForm(
                data=request.POST, instance=request.user.staff_profile)
        if user_form.is_valid() and personal_profile_form.is_valid():
            user_form.save()
            personal_profile_form.save()
            messages.success(request, 'Profile Updated Successfully.')
            return HttpResponseRedirect(reverse('account:view_update_profile'))
    context.update(
        {'user_form': user_form, 'personal_profile_form': personal_profile_form})
    return render(request, 'view_update_profile.html', context)
