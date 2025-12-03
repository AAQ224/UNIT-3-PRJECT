from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, LoginForm, ParentChildrenLinkForm
from .models import Profile, ParentStudentRelation
from courses.models import ClassSubject, StudentClassEnrollment
from django.http import HttpResponseForbidden
from progress.models import HomeworkSubmission, QuizSubmission


# Create your views here.


@login_required
def register(request):
    profile = getattr(request.user, "profile", None)

    if not (request.user.is_superuser or (profile and profile.role == "admin")):
        return HttpResponseForbidden("Only administrators can create new accounts.")

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

            messages.success(request, "Account created successfully.")
            return redirect('accounts:dashboard')
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

    is_admin = request.user.is_superuser or (profile and profile.role == 'admin')

    teacher_classes = []
    student_enrollment = None
    parent_children = []
    pending_homeworks = None
    pending_quizzes = None

    if role == 'teacher':
        teacher_classes = ClassSubject.objects.filter(teacher=request.user)

    elif role == 'student':
        student_enrollment = StudentClassEnrollment.objects.filter(
            student=request.user
        ).first()

        if student_enrollment:
            classsubjects = ClassSubject.objects.filter(
                school_class=student_enrollment.school_class
            )

            pending_homeworks = Homework.objects.filter(
                class_subject__in=classsubjects
            ).exclude(
                submissions__student=request.user
            ).count()

            pending_quizzes = Quiz.objects.filter(
                class_subject__in=classsubjects
            ).exclude(
                submissions__student=request.user
            ).count()
        else:
            pending_homeworks = 0
            pending_quizzes = 0

    elif role == 'parent':
        parent_children = ParentStudentRelation.objects.filter(parent=request.user)

    context = {
        'profile': profile,
        'role': role,
        'is_admin': is_admin,
        'teacher_classes': teacher_classes,
        'student_enrollment': student_enrollment,
        'parent_children': parent_children,
        'pending_homeworks': pending_homeworks,
        'pending_quizzes': pending_quizzes,
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

@login_required
def link_parent_children(request):
    profile = getattr(request.user, "profile", None)
    is_admin = request.user.is_superuser or (profile and profile.role == "admin")
    if not is_admin:
        return HttpResponseForbidden("Only administrators can link parents and children.")

    if request.method == "POST":
        form = ParentChildrenLinkForm(request.POST)
        if form.is_valid():
            parent = form.cleaned_data['parent']
            students = form.cleaned_data['students']

            for student in students:
                ParentStudentRelation.objects.get_or_create(
                    parent=parent,
                    student=student
                )

            messages.success(request, "Parent linked to selected children successfully.")
            return redirect("accounts:dashboard")
    else:
        form = ParentChildrenLinkForm()

    return render(request, "accounts/link_parent_children.html", {"form": form})
