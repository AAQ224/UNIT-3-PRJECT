from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from courses.models import ClassSubject, StudentClassEnrollment
from .models import Lesson, Homework, Quiz, HomeworkSubmission, QuizSubmission
from .forms import LessonForm, HomeworkForm, QuizForm
from django.http import HttpResponseForbidden
from accounts.models import ParentStudentRelation
from accounts.models import Profile


@login_required
def teacher_class_subject(request, classsubject_id):

    classsubject = get_object_or_404(ClassSubject, id=classsubject_id)

    if classsubject.teacher != request.user:
        messages.error(request, "Access to this subject's management is not allowed.")
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
        messages.error(request, "You are not authorized to create content for this subject.")
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.class_subject = classsubject
            lesson.save()
            messages.success(request, f"Lesson '{lesson.title}' created successfully.")
            return redirect('progress:teacher_class_subject', classsubject_id=classsubject.id)
    else:
        form = LessonForm()

    return render(request, "progress/lesson_form.html", {
        "form": form,
        "class  subject": classsubject,
        "mode": "create"
    })

@login_required
def lesson_update(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if lesson.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")
    
    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson updated successfully.")
            return redirect("progress:teacher_class_subject", classsubject_id=lesson.class_subject.id)
    else:
        form = LessonForm(instance=lesson)
        
    return render(request, "progress/lesson_form.html", {
        "form": form,
        "classsubject": lesson.class_subject,
        "mode": "update"
    })


@login_required
def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if lesson.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        lesson.delete()
        messages.success(request, f"Lesson '{lesson.title}' deleted successfully.")
        return redirect("progress:teacher_class_subject", classsubject_id=lesson.class_subject.id)
    
    return render(request, "progress/lesson_delete.html", {"lesson": lesson})


@login_required
def homework_create(request, classsubject_id):
    classsubject = get_object_or_404(ClassSubject, id=classsubject_id)
    if classsubject.teacher != request.user:
        messages.error(request, "You are not authorized to create content for this subject.")
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            hw = form.save(commit=False)
            hw.class_subject = classsubject
            hw.save()
            messages.success(request, f"Homework '{hw.title}' created successfully.")
            return redirect('progress:teacher_class_subject', classsubject_id=classsubject.id)
    else:
        form = HomeworkForm()

    return render(request, "progress/homework_form.html", {
        "form": form,
        "classsubject": classsubject,
        "mode": "create"
    })

@login_required
def homework_update(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    if homework.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")
    
    if request.method == "POST":
        form = HomeworkForm(request.POST, instance=homework)
        if form.is_valid():
            form.save()
            messages.success(request, "Homework updated successfully.")
            return redirect("progress:teacher_class_subject", classsubject_id=homework.class_subject.id)
    else:
        form = HomeworkForm(instance=homework)
        
    return render(request, "progress/homework_form.html", {
        "form": form,
        "classsubject": homework.class_subject,
        "mode": "update"
    })

@login_required
def homework_delete(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    if homework.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        homework.delete()
        messages.success(request, f"Homework '{homework.title}' deleted successfully.")
        return redirect("progress:teacher_class_subject", classsubject_id=homework.class_subject.id)
    
    return render(request, "progress/homework_delete.html", {"homework": homework})

@login_required
def quiz_create(request, classsubject_id):
    classsubject = get_object_or_404(ClassSubject, id=classsubject_id)
    if classsubject.teacher != request.user:
        messages.error(request, "You are not authorized to create content for this subject.")
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.class_subject = classsubject
            quiz.save()
            messages.success(request, f"Quiz '{quiz.title}' created successfully.")
            return redirect('progress:teacher_class_subject', classsubject_id=classsubject.id)
    else:
        form = QuizForm()

    return render(request, "progress/quiz_form.html", {
        "form": form,
        "classsubject": classsubject,
        "mode": "create"
    })


@login_required
def quiz_update(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")
    
    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, "Quiz updated successfully.")
            return redirect("progress:teacher_class_subject", classsubject_id=quiz.class_subject.id)
    else:
        form = QuizForm(instance=quiz)
        
    return render(request, "progress/quiz_form.html", {
        "form": form,
        "classsubject": quiz.class_subject,
        "mode": "update"
    })

@login_required
def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        quiz.delete()
        messages.success(request, f"Quiz '{quiz.title}' deleted successfully.")
        return redirect("progress:teacher_class_subject", classsubject_id=quiz.class_subject.id)
    
    return render(request, "progress/quiz_delete.html", {"quiz": quiz})


@login_required
def student_subject_detail(request, classsubject_id):
    classsubject = get_object_or_404(ClassSubject, id=classsubject_id)

    is_enrolled = StudentClassEnrollment.objects.filter(
        student=request.user,
        school_class=classsubject.school_class
    ).exists()

    if not is_enrolled:
        messages.error(request, "You are not enrolled in this class.")
        return HttpResponseForbidden("Not allowed")

    lessons = Lesson.objects.filter(class_subject=classsubject)
    homeworks = Homework.objects.filter(class_subject=classsubject)
    quizzes = Quiz.objects.filter(class_subject=classsubject)

    return render(request, "progress/student_subject_detail.html", {
        "classsubject": classsubject,
        "lessons": lessons,
        "homeworks": homeworks,
        "quizzes": quizzes,
    })


@login_required
def homework_submit(request, homework_id):
    hw = get_object_or_404(Homework, id=homework_id)

    is_enrolled = StudentClassEnrollment.objects.filter(
        student=request.user,
        school_class=hw.class_subject.school_class
    ).exists()

    if not is_enrolled:
        messages.error(request, "Access denied. You are not enrolled in the relevant class.")
        return HttpResponseForbidden("Not allowed")

    submission, created = HomeworkSubmission.objects.get_or_create(
        homework=hw,
        student=request.user,
        defaults={'answer_text': ''}
    )

    if request.method == "POST":
        answer = request.POST.get("answer_text", "")
        
        if answer.strip():
            submission.answer_text = answer
            submission.submitted_at = timezone.now()
            submission.save()
            messages.success(request, "Homework submitted/updated successfully.")
            return redirect("progress:student_subject_detail", classsubject_id=hw.class_subject.id)
        else:
            messages.error(request, "Submission text cannot be empty.")
            
    return render(request, "progress/homework_submit.html", {"homework": hw, "submission": submission})

@login_required
def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    is_enrolled = StudentClassEnrollment.objects.filter(
        student=request.user,
        school_class=quiz.class_subject.school_class
    ).exists()

    if not is_enrolled:
        messages.error(request, "Access denied. You are not enrolled in the relevant class.")
        return HttpResponseForbidden("Not allowed")

    submission, created = QuizSubmission.objects.get_or_create(
        quiz=quiz,
        student=request.user,
        defaults={'answer_text': ''}
    )

    if request.method == "POST":
        answer = request.POST.get("answer_text", "")
        
        if answer.strip():
            submission.answer_text = answer
            submission.submitted_at = timezone.now()
            submission.save()
            messages.success(request, "Quiz submitted/updated successfully.")
            return redirect("progress:student_subject_detail", classsubject_id=quiz.class_subject.id)
        else:
            messages.error(request, "Submission text cannot be empty.")
            
    return render(request, "progress/quiz_submit.html", {"quiz": quiz, "submission": submission})


@login_required
def homework_submissions(request, homework_id):
    hw = get_object_or_404(Homework, id=homework_id)

    if hw.class_subject.teacher != request.user:
        messages.error(request, "You are not authorized to view these submissions.")
        return HttpResponseForbidden("Not allowed")

    submissions = HomeworkSubmission.objects.filter(homework=hw).select_related('student__profile')

    return render(request, "progress/homework_submissions.html", {
        "homework": hw,
        "submissions": submissions,
    })

@login_required
def grade_homework_submission(request, submission_id):
    sub = get_object_or_404(HomeworkSubmission, id=submission_id)
    hw = sub.homework

    if hw.class_subject.teacher != request.user:
        messages.error(request, "You are not authorized to grade this submission.")
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        grade_value = request.POST.get("grade")
        
        if grade_value and grade_value.strip():
            try:
                grade = int(grade_value.strip())
                sub.grade = grade
                sub.save()
                messages.success(request, f"Grade {grade} saved successfully for {sub.student.username}.")
            except ValueError:
                messages.error(request, "Invalid grade value. Please enter a number.")
        else:
            sub.grade = None
            sub.save()
            messages.info(request, "Grade cleared successfully.")
            
        return redirect("progress:homework_submissions", homework_id=hw.id)

    return render(request, "progress/grade_homework.html", {
        "submission": sub,
        "homework": hw,
    })

@login_required
def quiz_submissions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.class_subject.teacher != request.user:
        messages.error(request, "You are not authorized to view these submissions.")
        return HttpResponseForbidden("Not allowed")

    submissions = QuizSubmission.objects.filter(quiz=quiz).select_related('student__profile')

    return render(request, "progress/quiz_submissions.html", {
        "quiz": quiz,
        "submissions": submissions,
    })


@login_required
def grade_quiz_submission(request, submission_id):
    sub = get_object_or_404(QuizSubmission, id=submission_id)
    quiz = sub.quiz

    if quiz.class_subject.teacher != request.user:
        messages.error(request, "You are not authorized to grade this submission.")
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        grade_value = request.POST.get("grade")
        
        if grade_value and grade_value.strip():
            try:
                grade = int(grade_value.strip())
                sub.grade = grade
                sub.save()
                messages.success(request, f"Grade {grade} saved successfully for {sub.student.username}.")
            except ValueError:
                messages.error(request, "Invalid grade value. Please enter a number.")
        else:
            sub.grade = None
            sub.save()
            messages.info(request, "Grade cleared successfully.")
            
        return redirect("progress:quiz_submissions", quiz_id=quiz.id)

    return render(request, "progress/grade_quiz.html", {
        "submission": sub,
        "quiz": quiz,
    })
