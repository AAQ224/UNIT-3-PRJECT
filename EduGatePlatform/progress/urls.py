from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('teacher/classsubject/<int:classsubject_id>/', views.teacher_class_subject, name='teacher_class_subject'),
    path('teacher/classsubject/<int:classsubject_id>/lesson/create/', views.lesson_create, name='lesson_create'),
    path('teacher/classsubject/<int:classsubject_id>/homework/create/', views.homework_create, name='homework_create'),
    path('teacher/classsubject/<int:classsubject_id>/quiz/create/', views.quiz_create, name='quiz_create'),
]
