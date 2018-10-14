from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
# Create your views here.


@login_required
def dashboard(request):
    context = {'request': request}
    return render(request, 'dashboard.html', context)


@login_required
def change_password(request):
    context = {'request': request}
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
