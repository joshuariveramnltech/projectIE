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
    path('student/view/schedule/', views.view_schedule_student,
         name='view_schedule_student'),
    path('student/subject/registration/',
         views.student_registration, name='student_registration'),
    path('faculty/view/students/chair/',
         views.view_all_students_chairperson, name='view_all_students_chairperson'),
    path('faculty/student/tagging/<int:student_id>/<student_username>/',
         views.student_tagging, name='student_tagging'),
    path('faculty/student/untagging/<int:subject_grade_id>/<int:student_id>/<student_username>/',
         views.remove_subject_chairperson, name='remove_subject_chairperson'),
]
