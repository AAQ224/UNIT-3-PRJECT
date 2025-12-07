from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import StudentClassEnrollment
from .forms import ClassSubjectForm, StudentMultiEnrollmentForm
from django.contrib import messages
from .models import Subject, ClassSubject
from .forms import SubjectForm

# Create your views here.

def is_admin(user):
    return user.is_superuser or hasattr(user, "profile") and user.profile.role == "admin"

@login_required
def classsubject_create(request):
    profile = getattr(request.user, "profile", None)
    is_admin = request.user.is_superuser or (profile and profile.role == "admin")
    if not is_admin:
        return HttpResponseForbidden("Only administrators can assign subjects.")

    if request.method == "POST":
        form = ClassSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("courses:classsubject_list")
    else:
        form = ClassSubjectForm()

    return render(request, "courses/classsubject_create.html", {"form": form})


@login_required
def enroll_students_in_class(request):
    profile = getattr(request.user, "profile", None)
    is_admin = request.user.is_superuser or (profile and profile.role == "admin")
    if not is_admin:
        return HttpResponseForbidden("Only administrators can enroll students.")

    if request.method == "POST":
        form = StudentMultiEnrollmentForm(request.POST)
        if form.is_valid():
            school_class = form.cleaned_data['school_class']
            students = form.cleaned_data['students']

            for student in students:
                StudentClassEnrollment.objects.get_or_create(
                    school_class=school_class,
                    student=student
                )

            return redirect("accounts:dashboard")
    else:
        form = StudentMultiEnrollmentForm()

    return render(request, "courses/enroll_student.html", {"form": form})

@login_required
def manage_enrollments(request):
    profile = getattr(request.user, "profile", None)
    is_admin = request.user.is_superuser or (profile and profile.role == "admin")
    if not is_admin:
        return HttpResponseForbidden("Not allowed")

    enrollments = StudentClassEnrollment.objects.select_related(
        "school_class",
        "student__profile",
    ).order_by("school_class__name", "student__username")

    return render(request, "courses/manage_enrollments.html", {
        "enrollments": enrollments,
    })


@login_required
def delete_enrollment(request, enrollment_id):
    profile = getattr(request.user, "profile", None)
    is_admin = request.user.is_superuser or (profile and profile.role == "admin")
    if not is_admin:
        return HttpResponseForbidden("Only administrators can manage enrollments.")

    enrollment = get_object_or_404(StudentClassEnrollment, id=enrollment_id)

    if request.method == "POST":
        enrollment.delete()
        messages.success(request, "Enrollment deleted successfully.")
        return redirect("courses:manage_enrollments")

    messages.error(request, "Invalid request method.")
    return redirect("courses:manage_enrollments")



@login_required
@user_passes_test(is_admin)
def subject_list(request):
    subjects = Subject.objects.all().order_by("name")
    return render(request, "courses/subject_list.html", {"subjects": subjects})


@login_required
@user_passes_test(is_admin)
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject created successfully.")
            return redirect("courses:subject_list")
    else:
        form = SubjectForm()
    return render(request, "courses/subject_form.html", {"form": form, "mode": "create"})


@login_required
@user_passes_test(is_admin)
def subject_update(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect("courses:subject_list")
    else:
        form = SubjectForm(instance=subject)
    return render(request, "courses/subject_form.html", {"form": form, "mode": "edit"})


@login_required
@user_passes_test(is_admin)
def subject_delete(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == "POST":
        name = subject.name
        subject.delete()
        messages.success(request, f"Subject '{name}' deleted.")
        return redirect("courses:subject_list")
        
    return render(request, "courses/subject_delete.html", {"subject": subject})

@login_required
@user_passes_test(is_admin)
def classsubject_list(request):
    classsubjects = ClassSubject.objects.all().select_related('school_class', 'subject', 'teacher').order_by('school_class__name', 'subject__name')
    return render(request, "courses/classsubject_list.html", {"classsubjects": classsubjects})

@login_required
@user_passes_test(is_admin)
def classsubject_update(request, pk):
    classsubject = get_object_or_404(ClassSubject, pk=pk)

    if request.method == 'POST':
        form = ClassSubjectForm(request.POST, instance=classsubject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject assignment updated successfully.")
            return redirect('courses:classsubject_list')
    else:
        form = ClassSubjectForm(instance=classsubject)
        
    context = {
        'form': form,
        'assignment': classsubject,
    }
    return render(request, 'courses/classsubject_form.html', context)

@login_required
@user_passes_test(is_admin)
def classsubject_delete(request, pk):
    classsubject = get_object_or_404(ClassSubject, pk=pk)
    
    if request.method == 'POST':
        assignment_info = f"'{classsubject.subject.name}' to '{classsubject.school_class.name}'"
        classsubject.delete()
        messages.success(request, f"Assignment {assignment_info} has been deleted.")
        return redirect('courses:classsubject_list')
        
    context = {
        'assignment': classsubject,
    }
    return render(request, 'courses/classsubject_delete.html', context)