from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('teacher/classsubject/<int:classsubject_id>/', views.teacher_class_subject, name='teacher_class_subject'),
    path('teacher/classsubject/<int:classsubject_id>/lesson/create/', views.lesson_create, name='lesson_create'),
    path('teacher/classsubject/<int:classsubject_id>/homework/create/', views.homework_create, name='homework_create'),
    path('teacher/classsubject/<int:classsubject_id>/quiz/create/', views.quiz_create, name='quiz_create'),
    path('student/subject/<int:classsubject_id>/', views.student_subject_detail, name='student_subject_detail'),
    path('student/homework/<int:homework_id>/submit/', views.homework_submit, name='homework_submit'),
    path('student/quiz/<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    path('teacher/homework/<int:homework_id>/submissions/', views.homework_submissions, name='homework_submissions'),
    path('teacher/homework/submission/<int:submission_id>/grade/', views.grade_homework_submission, name='grade_homework_submission'),
    path('teacher/quiz/<int:quiz_id>/submissions/', views.quiz_submissions, name='quiz_submissions'),
    path('teacher/quiz/submission/<int:submission_id>/grade/', views.grade_quiz_submission, name='grade_quiz_submission'),

]
