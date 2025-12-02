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

]
