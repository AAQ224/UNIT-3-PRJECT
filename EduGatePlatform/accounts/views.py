from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, LoginForm
from .models import Profile
from courses.models import ClassSubject, StudentClassEnrollment
from .models import ParentStudentRelation


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
