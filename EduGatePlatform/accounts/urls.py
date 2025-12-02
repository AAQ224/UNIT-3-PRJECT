from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/subjects/', views.student_subjects, name='student_subjects'),
    path('student/grades/', views.student_grades, name='student_grades'),
    path('parent/child/<int:student_id>/grades/', views.parent_child_grades, name='parent_child_grades'),

]
