from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import ClassSubject
from .models import Lesson, Homework, Quiz
from .forms import LessonForm, HomeworkForm, QuizForm
from django.http import HttpResponseForbidden

# Create your views here.

@login_required
def teacher_class_subject(request, classsubject_id):

    classsubject = get_object_or_404(ClassSubject, id=classsubject_id)

    if classsubject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    lessons = Lesson.objects.filter(class_subject=classsubject)
    homeworks = Homework.objects.filter(class_subject=classsubject)
    quizzes = Quiz.objects.filter(class_subject=classsubject)

    return render(request, "progress/teacher_class_subject.html", {
        "classsubject": classsubject,
        "lessons": lessons,
        "homeworks": homeworks,
        "quizzes": quizzes,
    })

@login_required
def lesson_create(request, classsubject_id):
    classsubject = get_object_or_404(ClassSubject, id=classsubject_id)
    if classsubject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.class_subject = classsubject
            lesson.save()
            return redirect('progress:teacher_class_subject', classsubject_id=classsubject.id)
    else:
        form = LessonForm()

    return render(request, "progress/lesson_form.html", {
        "form": form,
        "classsubject": classsubject,
    })


@login_required
def homework_create(request, classsubject_id):
    classsubject = get_object_or_404(ClassSubject, id=classsubject_id)
    if classsubject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            hw = form.save(commit=False)
            hw.class_subject = classsubject
            hw.save()
            return redirect('progress:teacher_class_subject', classsubject_id=classsubject.id)
    else:
        form = HomeworkForm()

    return render(request, "progress/homework_form.html", {
        "form": form,
        "classsubject": classsubject,
    })


@login_required
def quiz_create(request, classsubject_id):
    classsubject = get_object_or_404(ClassSubject, id=classsubject_id)
    if classsubject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.class_subject = classsubject
            quiz.save()
            return redirect('progress:teacher_class_subject', classsubject_id=classsubject.id)
    else:
        form = QuizForm()

    return render(request, "progress/quiz_form.html", {
        "form": form,
        "classsubject": classsubject,
    })

