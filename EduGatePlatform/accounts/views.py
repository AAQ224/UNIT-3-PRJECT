from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, LoginForm
from .models import Profile, ParentStudentRelation
from courses.models import ClassSubject, StudentClassEnrollment
from django.http import HttpResponseForbidden
from progress.models import HomeworkSubmission, QuizSubmission


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password) 
            user.save()

            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                national_id=form.cleaned_data['national_id'],
                role=form.cleaned_data['role']
            )

            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = LoginForm(request)

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('main:home')


@login_required
def dashboard(request):
    profile = getattr(request.user, 'profile', None)
    role = profile.role if profile else 'unknown'

    teacher_classes = []
    student_enrollment = None
    parent_children = []

    if role == 'teacher':
        teacher_classes = ClassSubject.objects.filter(teacher=request.user)

    elif role == 'student':
        student_enrollment = StudentClassEnrollment.objects.filter(
            student=request.user
        ).first()

    elif role == 'parent':
        parent_children = ParentStudentRelation.objects.filter(parent=request.user)

    context = {
        'profile': profile,
        'role': role,
        'teacher_classes': teacher_classes,
        'student_enrollment': student_enrollment,
        'parent_children': parent_children,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def student_subjects(request):
    profile = request.user.profile

    if profile.role != "student":
        return HttpResponseForbidden("Not allowed")

    enrollment = StudentClassEnrollment.objects.filter(student=request.user).first()

    classsubjects = []
    if enrollment:
        classsubjects = ClassSubject.objects.filter(school_class=enrollment.school_class)

    return render(request, "accounts/student_subjects.html", {
        "classsubjects": classsubjects,
        "enrollment": enrollment,
    })

@login_required
def student_grades(request):
    profile = request.user.profile
    if profile.role != "student":
        return HttpResponseForbidden("Not allowed")

    hw_subs = HomeworkSubmission.objects.filter(student=request.user).select_related(
        'homework__class_subject__subject'
    )
    quiz_subs = QuizSubmission.objects.filter(student=request.user).select_related(
        'quiz__class_subject__subject'
    )

    return render(request, "accounts/student_grades.html", {
        "hw_subs": hw_subs,
        "quiz_subs": quiz_subs,
    })

@login_required
def parent_child_grades(request, student_id):
    profile = request.user.profile
    if profile.role != "parent":
        return HttpResponseForbidden("Not allowed")

    relation_exists = ParentStudentRelation.objects.filter(
        parent=request.user,
        student__id=student_id
    ).exists()

    if not relation_exists:
        return HttpResponseForbidden("Not allowed")

    student = get_object_or_404(User, id=student_id)

    hw_subs = HomeworkSubmission.objects.filter(student=student).select_related(
        'homework__class_subject__subject'
    )
    quiz_subs = QuizSubmission.objects.filter(student=student).select_related(
        'quiz__class_subject__subject'
    )

    return render(request, "accounts/parent_child_grades.html", {
        "student": student,
        "hw_subs": hw_subs,
        "quiz_subs": quiz_subs,
    })
