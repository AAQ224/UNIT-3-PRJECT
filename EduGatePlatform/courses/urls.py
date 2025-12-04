from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    
    path("enroll-student/", views.enroll_students_in_class, name="enroll_student"),
    
    path("subjects/", views.subject_list, name="subject_list"),
    path("subjects/create/", views.subject_create, name="subject_create"),
    path("subjects/<int:subject_id>/edit/", views.subject_update, name="subject_update"),
    path("subjects/<int:subject_id>/delete/", views.subject_delete, name="subject_delete"),
    
    path('assignments/', views.classsubject_list, name='classsubject_list'),
    path('assignments/create/', views.classsubject_create, name='classsubject_create'), 
    path('assignments/update/<int:pk>/', views.classsubject_update, name='classsubject_update'), 
    path('assignments/delete/<int:pk>/', views.classsubject_delete, name='classsubject_delete'), 
]