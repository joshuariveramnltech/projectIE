from django import forms
from .models import SubjectGrade


class UpdateSubjectGrade(forms.ModelForm):
    class Meta:
        model = SubjectGrade
        fields = ['final_grade', 'is_finalized']
