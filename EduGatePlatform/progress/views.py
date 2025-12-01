from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import ClassSubject
from .models import Lesson, Homework, Quiz

# Create your views here.

@login_required
def teacher_class_subject(request, classsubject_id):
    classsubject = get_object_or_404(ClassSubject, id=classsubject_id)

    lessons = Lesson.objects.filter(class_subject=classsubject)
    homeworks = Homework.objects.filter(class_subject=classsubject)
    quizzes = Quiz.objects.filter(class_subject=classsubject)

    return render(request, "progress/teacher_class_subject.html", {
        "classsubject": classsubject,
        "lessons": lessons,
        "homeworks": homeworks,
        "quizzes": quizzes,
    })
