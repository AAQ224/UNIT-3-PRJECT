from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('teacher/classsubject/<int:classsubject_id>/', views.teacher_class_subject, name='teacher_class_subject'),
    
    # Lesson URLs
    path('teacher/classsubject/<int:classsubject_id>/lesson/create/', views.lesson_create, name='lesson_create'),
    path('teacher/lesson/<int:lesson_id>/update/', views.lesson_update, name='lesson_update'),
    path('teacher/lesson/<int:lesson_id>/delete/', views.lesson_delete, name='lesson_delete'),
    
    # Homework URLs
    path('teacher/classsubject/<int:classsubject_id>/homework/create/', views.homework_create, name='homework_create'),
    path('teacher/homework/<int:homework_id>/update/', views.homework_update, name='homework_update'),
    path('teacher/homework/<int:homework_id>/delete/', views.homework_delete, name='homework_delete'),
    
    # Quiz URLs
    path('teacher/classsubject/<int:classsubject_id>/quiz/create/', views.quiz_create, name='quiz_create'),
    path('teacher/quiz/<int:quiz_id>/update/', views.quiz_update, name='quiz_update'),
    path('teacher/quiz/<int:quiz_id>/delete/', views.quiz_delete, name='quiz_delete'),

    path('student/subject/<int:classsubject_id>/', views.student_subject_detail, name='student_subject_detail'),
    path('student/homework/<int:homework_id>/submit/', views.homework_submit, name='homework_submit'),
    path('student/quiz/<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    path('teacher/homework/<int:homework_id>/submissions/', views.homework_submissions, name='homework_submissions'),
    path('teacher/homework/submission/<int:submission_id>/grade/', views.grade_homework_submission, name='grade_homework_submission'),
    path('teacher/quiz/<int:quiz_id>/submissions/', views.quiz_submissions, name='quiz_submissions'),
    path('teacher/quiz/submission/<int:submission_id>/grade/', views.grade_quiz_submission, name='grade_quiz_submission'),

    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('attempts/<int:attempt_id>/take/', views.take_quiz, name='take_quiz'),
    path('attempts/<int:attempt_id>/result/', views.attempt_result, name='attempt_result'),

        path('quizzes/<int:quiz_id>/questions/', views.quiz_questions_manage, name='quiz_questions_manage'),
    path('quizzes/<int:quiz_id>/questions/create/', views.question_create, name='question_create'),
    path('questions/<int:question_id>/edit/', views.question_update, name='question_update'),
    path('questions/<int:question_id>/delete/', views.question_delete, name='question_delete'),

    path('questions/<int:question_id>/choices/create/', views.choice_create, name='choice_create'),
    path('choices/<int:choice_id>/edit/', views.choice_update, name='choice_update'),
    path('choices/<int:choice_id>/delete/', views.choice_delete, name='choice_delete'),


]