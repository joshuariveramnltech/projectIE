from django.urls import path
from . import views

# Create your url patterns

app_name = "grading_system"

urlpatterns = [
    # path('test/', views.test, name='test'),
    path('student/view/all/grades/', views.view_all_grades, name='view_all_grades'),
    path('faculty/view/assigned/subject-s/',
         views.view_assigned_subjects, name='view_assigned_subjects'),
    path('faculty/view/students/per-subject/<int:subject_instance_id>/<subject_code>/',
         views.view_students_per_subject, name='view_students_per_subject'),
    path('faculty/view/update/subject/grade/<int:subject_grade_id>/',
         views.view_update_grade, name='view_update_grade'),
]
