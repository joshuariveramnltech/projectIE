from django.shortcuts import render
from .models import SubjectInstance


# Create your views here.

def test(request):
    subjects = SubjectInstance.objects.all().distinct('school_year')
    context = {'request': request, 'subjects': subjects}
    return render(request, 'test.html', context)
