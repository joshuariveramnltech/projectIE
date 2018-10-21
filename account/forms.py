from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import ACCOUNT_TYPE_CHOICES
from .models import (
    StudentProfile, FacultyProfile, StaffProfile
)

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    account_type = forms.ChoiceField(
        label='Account Type', choices=ACCOUNT_TYPE_CHOICES)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = []
        unique_together = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 is not None and password1 is not None and password1 != password2:
            raise forms.ValidationError('Password don\'t match!')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if self.cleaned_data.get('account_type') == 'Administrator':
            user.is_staff = user.is_superuser = True
        elif self.cleaned_data['account_type'] == 'Staff':
            user.is_staff = True
        elif self.cleaned_data['account_type'] == 'Student':
            user.is_student = True
        elif self.cleaned_data['account_type'] == 'Faculty':
            user.is_faculty = True
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = []
        labels = {'account_type': 'Change Account Type'}
        unique_together = ('username', 'email')

    password = ReadOnlyPasswordHashField()
    account_type = forms.ChoiceField(
        label='Account Type', choices=ACCOUNT_TYPE_CHOICES, initial='')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        proxy_type = self.cleaned_data.get('account_type')
        if proxy_type == 'Administrator':
            user.is_staff = user.is_superuser = True
        elif proxy_type == 'Staff':
            user.is_staff = True
            user.is_superuser = False
        elif proxy_type == 'Student':
            user.is_superuser = user.is_staff = user.is_faculty = False
            user.is_student = True
        elif proxy_type == 'Faculty':
            user.is_superuser = user.is_staff = user.is_student = False
            user.is_faculty = True
        else:
            pass  # do nothing
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm  # create view
    form = UserChangeForm  # update view

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [
        'username', 'email',
        'is_active', 'is_superuser',
        'is_staff', 'is_faculty', 'is_student'
    ]
    list_filter = ['is_active', 'is_staff',
                   'is_superuser', 'is_student', 'is_faculty']
    fieldsets = (
        ('Credentials', {'fields': ('username', 'email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'middle_name', 'last_name',
                                             'birth_date', 'gender', 'address', 'photo', 'phone_number')
                                  }
         ),
        (
            'Account Status', {
                'fields': ('is_active', 'account_type',)
            }
        )
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'username', 'email', 'first_name', 'middle_name', 'last_name',
                    'birth_date', 'gender', 'address', 'photo', 'phone_number', 'is_active', 'account_type',
                    'password1', 'password2'
                ),
            }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# for personal use only
class PersonalUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = [
            'username', 'first_name', 'last_name',
            'middle_name', 'is_staff', 'is_superuser',
            'last_login', 'password', 'is_active'
        ]


# for faculty personal use
class PersonalFacultyForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        exclude = [
            'user', 'department',
            'is_chairperson', 'status', 'updated', 'date_joined'
        ]


# for staff personal use
class PersonalStaffForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        exclude = [
            'user', 'date_joined', 'updated',
        ]


# for student personal use
class PersonalStudentForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'guardian', 'additional_information',
        ]
