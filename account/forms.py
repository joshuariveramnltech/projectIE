from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

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
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        exclude = []
        unique_together = ('username', 'email')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm  # create view
    form = UserChangeForm  # update view

    list_display = [
        'username', 'email',
        'is_active', 'is_superuser',
        'is_staff'
    ]
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (
            'Personal Information', {
                'fields': ('first_name', 'middle_name', 'last_name', 'birthday', 'gender', 'address')
            }
        ),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'username', 'email', 'first_name', 'middle_name', 'last_name',
                    'birthday', 'gender', 'address', 'is_active',
                    'is_staff', 'is_superuser', 'password1', 'password2'
                ),
            }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
