from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden

from courses.models import ClassSubject, StudentClassEnrollment
from .models import (
    Lesson,
    Homework,
    Quiz,
    HomeworkSubmission,
    QuizSubmission,
    Question,
    Choice,
    QuizAttempt,
    Answer,
)
from .forms import LessonForm, HomeworkForm, QuizForm, QuestionForm, ChoiceForm
from accounts.models import ParentStudentRelation, Profile


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
        "classsubject": classsubject,   # أصلحنا الكي هنا
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

    # تأكد إن الطالب مسجل في نفس الكلاس
    is_enrolled = StudentClassEnrollment.objects.filter(
        student=request.user,
        school_class=classsubject.school_class
    ).exists()

    if not is_enrolled:
        messages.error(request, "You are not enrolled in this class.")
        return HttpResponseForbidden("Not allowed")

    # الدروس + الواجبات + الكويزات
    lessons = Lesson.objects.filter(class_subject=classsubject)
    homeworks = Homework.objects.filter(class_subject=classsubject)
    quizzes = Quiz.objects.filter(class_subject=classsubject)

    # ⚠️ هنا أهم شي: نستخدم تيمبلت accounts اللي انت عدلته
    return render(request, "accounts/student_subject_detail.html", {
        "class_subject": classsubject,  # نفس الاسم اللي في التيمبلت حقك
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
    """
    هذا الفيو القديم لكويز نصّي (إجابة نصية واحدة).
    نخليه كما هو لو تحتاجه لنوع معيّن من الكويزات.
    النظام الجديد (أسئلة/خيارات) له فيوهات ثانية تحت.
    """
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
    """
    هذا الفيو ما زال يعرض تسليمات QuizSubmission (النصية).
    للسيستم الجديد (QuizAttempt) أضفنا فيو quiz_attempts تحت.
    """
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

@login_required
def start_quiz_attempt(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    is_enrolled = StudentClassEnrollment.objects.filter(
        student=request.user,
        school_class=quiz.class_subject.school_class
    ).exists()

    if not is_enrolled:
        messages.error(request, "Access denied. You are not enrolled in the relevant class.")
        return HttpResponseForbidden("Not allowed")

    now = timezone.now()

    if quiz.start_time and now < quiz.start_time:
        return render(request, "progress/not_available.html", {
            "message": "لم يبدأ الاختبار بعد."
        })

    if quiz.end_time and now > quiz.end_time:
        return render(request, "progress/not_available.html", {
            "message": "انتهى وقت هذا الاختبار."
        })

    previous_attempts = QuizAttempt.objects.filter(
        quiz=quiz,
        student=request.user
    ).order_by('-id')

    attempts_count = previous_attempts.count()

    if quiz.max_attempts and quiz.max_attempts > 0 and attempts_count >= quiz.max_attempts:
        last_attempt = previous_attempts.first()
        return render(request, "progress/not_available.html", {
            "message": f"لقد وصلت إلى الحد الأقصى لعدد المحاولات المسموح بها لهذا الاختبار ({quiz.max_attempts}).",
            "last_attempt": last_attempt,
        })

    attempt = QuizAttempt.objects.create(
        quiz=quiz,
        student=request.user
    )

    return redirect("progress:take_quiz_attempt", attempt_id=attempt.id)


@login_required
def take_quiz_attempt(request, attempt_id):

    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    quiz = attempt.quiz

    if quiz.duration_minutes:
        deadline = attempt.started_at + timedelta(minutes=quiz.duration_minutes)
    else:
        deadline = quiz.end_time

    now = timezone.now()

    if deadline and now > deadline and not attempt.is_submitted:
        attempt.is_submitted = True
        attempt.finished_at = now
        attempt.save()
        return render(request, "progress/not_available.html", {
            "message": "انتهى وقت هذا الاختبار."
        })

    if attempt.is_submitted:
        return render(request, "progress/already_submitted.html", {
            "attempt": attempt,
        })

    if request.method == "POST":
        attempt.answers.all().delete()

        for q in quiz.questions.all():
            ans = Answer.objects.create(attempt=attempt, question=q)

            if q.qtype in [Question.SINGLE, Question.MULTI]:
                selected_ids = request.POST.getlist(f"question_{q.id}")
                choices = Choice.objects.filter(
                    id__in=selected_ids,
                    question=q
                )
                ans.selected_choices.set(choices)

            elif q.qtype == Question.TEXT:
                text_value = request.POST.get(f"question_{q.id}_text", "").strip()
                ans.text_answer = text_value
                ans.save()

        total_points = 0
        earned = 0

        for q in quiz.questions.all():
            total_points += q.points
            ans = attempt.answers.get(question=q)

            if q.qtype == Question.SINGLE:
                selected = ans.selected_choices.first()
                if selected and selected.is_correct:
                    earned += q.points

            elif q.qtype == Question.MULTI:
                correct_ids = set(
                    q.choices.filter(is_correct=True).values_list('id', flat=True)
                )
                selected_ids = set(
                    ans.selected_choices.values_list('id', flat=True)
                )
                if selected_ids == correct_ids:
                    earned += q.points


        attempt.score = (earned / total_points * 100) if total_points > 0 else 0
        attempt.is_submitted = True
        attempt.finished_at = timezone.now()
        attempt.save()

        return redirect("progress:quiz_attempt_result", attempt_id=attempt.id)

    return render(request, "progress/take_quiz.html", {
        "quiz": quiz,
        "attempt": attempt,
        "deadline": deadline,
    })


@login_required
def quiz_attempt_result(request, attempt_id):

    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)

    return render(request, "progress/attempt_result.html", {"attempt": attempt,})


@login_required
def quiz_attempts(request, quiz_id):
    """
    عرض جميع المحاولات على كويز معيّن (للمعلم).
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.class_subject.teacher != request.user:
        messages.error(request, "You are not authorized to view these attempts.")
        return HttpResponseForbidden("Not allowed")

    attempts = QuizAttempt.objects.filter(
        quiz=quiz
    ).select_related('student__profile').order_by('-started_at')

    return render(request, "progress/quiz_attempts.html", {
        "quiz": quiz,
        "attempts": attempts,
    })


@login_required
def quiz_attempt_detail(request, attempt_id):
    """
    تفاصيل محاولة معينة (للمعلم) مع كل الإجابات.
    """
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    quiz = attempt.quiz

    if quiz.class_subject.teacher != request.user:
        messages.error(request, "You are not authorized to view this attempt.")
        return HttpResponseForbidden("Not allowed")

    return render(request, "progress/quiz_attempt_detail.html", {
        "quiz": quiz,
        "attempt": attempt,
    })

@login_required
def quiz_list(request):
   
    quizzes = Quiz.objects.filter(is_active=True).order_by('-created_at')
    return render(request, "progress/quiz_list.html", {
        "quizzes": quizzes,
    })


@login_required
def quiz_detail(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    attempts = QuizAttempt.objects.filter(
        quiz=quiz,
        student=request.user,
        is_submitted=True
    ).order_by('-started_at')

    return render(request, "progress/quiz_detail.html", {
        "quiz": quiz,
        "attempts": attempts,
    })


@login_required
def start_quiz(request, quiz_id):

    return start_quiz_attempt(request, quiz_id)


@login_required
def take_quiz(request, attempt_id):

    return take_quiz_attempt(request, attempt_id)


@login_required
def attempt_result(request, attempt_id):

    return quiz_attempt_result(request, attempt_id)

@login_required
def quiz_questions_manage(request, quiz_id):
    """
    صفحة للمعلم تعرض كل الأسئلة والخيارات لكويز معيّن.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # تأكد أن اللي داخل هو المعلم صاحب المادة
    if quiz.class_subject.teacher != request.user:
        messages.error(request, "You are not authorized to manage questions for this quiz.")
        return HttpResponseForbidden("Not allowed")

    questions = quiz.questions.all().prefetch_related('choices')

    return render(request, "progress/quiz_questions_manage.html", {
        "quiz": quiz,
        "questions": questions,
    })


@login_required
def question_create(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, "Question created successfully.")
            return redirect("progress:quiz_questions_manage", quiz_id=quiz.id)
    else:
        form = QuestionForm()

    return render(request, "progress/question_form.html", {
        "form": form,
        "quiz": quiz,
        "mode": "create",
    })


@login_required
def question_update(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz

    if quiz.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated successfully.")
            return redirect("progress:quiz_questions_manage", quiz_id=quiz.id)
    else:
        form = QuestionForm(instance=question)

    return render(request, "progress/question_form.html", {
        "form": form,
        "quiz": quiz,
        "mode": "update",
    })


@login_required
def question_delete(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz

    if quiz.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        question.delete()
        messages.success(request, "Question deleted successfully.")
        return redirect("progress:quiz_questions_manage", quiz_id=quiz.id)

    return render(request, "progress/question_delete.html", {
        "quiz": quiz,
        "question": question,
    })


@login_required
def choice_create(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz

    if quiz.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            messages.success(request, "Choice created successfully.")
            return redirect("progress:quiz_questions_manage", quiz_id=quiz.id)
    else:
        form = ChoiceForm()

    return render(request, "progress/choice_form.html", {
        "form": form,
        "quiz": quiz,
        "question": question,
        "mode": "create",
    })


@login_required
def choice_update(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    question = choice.question
    quiz = question.quiz

    if quiz.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            messages.success(request, "Choice updated successfully.")
            return redirect("progress:quiz_questions_manage", quiz_id=quiz.id)
    else:
        form = ChoiceForm(instance=choice)

    return render(request, "progress/choice_form.html", {
        "form": form,
        "quiz": quiz,
        "question": question,
        "mode": "update",
    })


@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    question = choice.question
    quiz = question.quiz

    if quiz.class_subject.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        choice.delete()
        messages.success(request, "Choice deleted successfully.")
        return redirect("progress:quiz_questions_manage", quiz_id=quiz.id)

    return render(request, "progress/choice_delete.html", {
        "quiz": quiz,
        "question": question,
        "choice": choice,
    })