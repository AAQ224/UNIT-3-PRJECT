from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, LoginForm, ParentChildrenLinkForm, UserEditForm
from .models import Profile, ParentStudentRelation
from courses.models import ClassSubject, StudentClassEnrollment, SchoolClass
from django.http import HttpResponseForbidden
from progress.models import HomeworkSubmission, QuizSubmission,Quiz,Homework,QuizAttempt


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

            role = form.cleaned_data['role']

            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True

            user.save()

            role = form.cleaned_data['role']

            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                national_id=form.cleaned_data['national_id'],
                role=role
            )

            if role == "admin":
                user.is_staff = True
                user.is_superuser = True
                user.save()


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
        teacher_classes = ClassSubject.objects.filter(teacher=request.user).select_related('school_class', 'subject')    
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

    homework_submissions = HomeworkSubmission.objects.filter(
        student=request.user
    ).select_related(
        'homework__class_subject__subject'
    ).order_by('-submitted_at')

    quiz_attempts = QuizAttempt.objects.filter(
        student=request.user,
        is_submitted=True
    ).select_related(
        'quiz__class_subject__subject'
    ).order_by('-finished_at', '-id') 

    return render(request, "accounts/student_grades.html", {
        "homework_submissions": homework_submissions,
        "quiz_attempts": quiz_attempts,
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

    quiz_attempts = QuizAttempt.objects.filter(
        student=student,
        is_submitted=True          
    ).select_related(
        'quiz__class_subject__subject'
    )

    return render(request, "accounts/parent_child_grades.html", {
        "student": student,
        "hw_subs": hw_subs,
        "quiz_attempts": quiz_attempts,   
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

@login_required
def manage_parent_links(request):
    profile = getattr(request.user, "profile", None)
    is_admin = request.user.is_superuser or (profile and profile.role == "admin")
    if not is_admin:
        return HttpResponseForbidden("Only administrators can manage parent links.")

    relations = ParentStudentRelation.objects.select_related(
        "parent__profile",
        "student__profile",
    ).order_by("parent__profile__full_name", "student__profile__full_name")

    context = {
        "relations": relations,
    }
    return render(request, "accounts/manage_parent_links.html", context)


@login_required
def delete_parent_link(request, relation_id):
    profile = getattr(request.user, "profile", None)
    is_admin = request.user.is_superuser or (profile and profile.role == "admin")
    if not is_admin:
        return HttpResponseForbidden("Only administrators can manage parent links.")

    relation = get_object_or_404(ParentStudentRelation, id=relation_id)

    if request.method == "POST":
        relation.delete()
        messages.success(request, "Parent–child link deleted successfully.")
        return redirect("accounts:manage_parent_links")

    messages.error(request, "Invalid request method.")
    return redirect("accounts:manage_parent_links")

@login_required
def manage_users(request):
    profile = getattr(request.user, "profile", None)
    is_admin = request.user.is_superuser or (profile and profile.role == "admin")
    if not is_admin:
        return HttpResponseForbidden("Only administrators can manage users.")

    profiles = Profile.objects.select_related("user").order_by("full_name")

    admins = [p for p in profiles if p.role == "admin"]
    teachers = [p for p in profiles if p.role == "teacher"]
    students = [p for p in profiles if p.role == "student"]
    parents = [p for p in profiles if p.role == "parent"]

    context = {
        "admins": admins,
        "teachers": teachers,
        "students": students,
        "parents": parents,
    }
    return render(request, "accounts/manage_users.html", context)


@login_required
def delete_user(request, user_id):
    profile = getattr(request.user, "profile", None)
    is_admin = request.user.is_superuser or (profile and profile.role == "admin")
    if not is_admin:
        return HttpResponseForbidden("Only administrators can delete users.")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        if user == request.user:
            messages.error(request, "You cannot delete your own account.")
            return redirect("accounts:manage_users")

        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect("accounts:manage_users")

    messages.error(request, "Invalid request method.")
    return redirect("accounts:manage_users")

@login_required
def edit_user(request, user_id):
    profile = getattr(request.user, "profile", None)
    is_admin = request.user.is_superuser or (profile and profile.role == "admin")
    if not is_admin:
        return HttpResponseForbidden("Only administrators can edit users.")

    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        form = UserEditForm(request.POST, user=user)
        if form.is_valid():
            user.username = form.cleaned_data["username"]
            user.email = form.cleaned_data["email"]
            user.is_active = form.cleaned_data["is_active"]
            user.save()

            user_profile.full_name = form.cleaned_data["full_name"]
            user_profile.national_id = form.cleaned_data["national_id"]
            user_profile.role = form.cleaned_data["role"]
            user_profile.save()

            messages.success(request, "User updated successfully.")
            return redirect("accounts:manage_users")
    else:
        form = UserEditForm(
            initial={
                "username": user.username,
                "email": user.email,
                "full_name": user_profile.full_name,
                "national_id": user_profile.national_id,
                "role": user_profile.role,
                "is_active": user.is_active,
            },
            user=user,
        )

    return render(request, "accounts/edit_user.html", {
        "form": form,
        "user_obj": user,
    })