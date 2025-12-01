from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('teacher/classsubject/<int:classsubject_id>/', views.teacher_class_subject, name='teacher_class_subject'),
]
