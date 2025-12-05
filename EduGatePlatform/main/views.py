from django.shortcuts import render, redirect, get_object_or_404 # Added get_object_or_404
from .models import Announcement
from django.utils import timezone
from django.db import models
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from accounts.models import Profile
from courses.models import SchoolClass
from .forms import SchoolClassForm, AnnouncementForm
from django.contrib import messages

# Create your views here.

def home(request):
    # ... (rest of home view) ...
    today = timezone.now().date()
    announcements = Announcement.objects.filter(
        models.Q(start_date__isnull=True) | (models.Q(start_date__lte=today)),
        models.Q(end_date__isnull=True) | (models.Q(end_date__gte=today))
    ).order_by('-is_important', '-created_at')[:6]

    context = {
        'announcements': announcements,
    }
    return render(request, 'main/home.html', context)

@login_required
def create_class(request):
    profile = getattr(request.user, "profile", None)

    if not (request.user.is_superuser or (profile and profile.role == "admin")):
        return HttpResponseForbidden("Only administrators can create classes.")

    if request.method == "POST":
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "School Class created successfully.") # Added message
            return redirect("main:schoolclass_list") # Redirect to list view
    else:
        form = SchoolClassForm()

    return render(request, "main/create_class.html", {"form": form})

# New view: School Class List
@login_required
def schoolclass_list(request):
    profile = getattr(request.user, "profile", None)

    if not (request.user.is_superuser or (profile and profile.role == "admin")):
        return HttpResponseForbidden("Only administrators can view school class list.")

    classes = SchoolClass.objects.all().order_by('grade_level', 'name')

    return render(request, "main/schoolclass_list.html", {"classes": classes})

# New view: School Class Update
@login_required
def schoolclass_update(request, class_id):
    profile = getattr(request.user, "profile", None)

    if not (request.user.is_superuser or (profile and profile.role == "admin")):
        return HttpResponseForbidden("Only administrators can edit classes.")

    school_class = get_object_or_404(SchoolClass, id=class_id)
    if request.method == "POST":
        form = SchoolClassForm(request.POST, instance=school_class)
        if form.is_valid():
            form.save()
            messages.success(request, "School Class updated successfully.")
            return redirect("main:schoolclass_list")
    else:
        form = SchoolClassForm(instance=school_class)

    return render(request, "main/create_class.html", {"form": form})

# New view: School Class Delete
@login_required
def schoolclass_delete(request, class_id):
    profile = getattr(request.user, "profile", None)

    if not (request.user.is_superuser or (profile and profile.role == "admin")):
        return HttpResponseForbidden("Only administrators can delete classes.")

    school_class = get_object_or_404(SchoolClass, id=class_id)
    if request.method == "POST":
        school_class.delete()
        messages.success(request, f"School Class '{school_class.name}' deleted successfully.")
        return redirect("main:schoolclass_list")

    return render(request, "main/schoolclass_delete.html", {"school_class": school_class})


@login_required
def add_announcement(request):
    profile = getattr(request.user, "profile", None)

    if not (request.user.is_superuser or (profile and profile.role == "admin")):
        return HttpResponseForbidden("Only administrators can add announcements.")

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement added successfully.")
            return redirect("main:home")
    else:
        form = AnnouncementForm()

    return render(request, "main/add_announcement.html", {"form": form, "page_title": "Add Announcement",
    })


@login_required
def announcement_list(request):
    profile = getattr(request.user, "profile", None)

    if not (request.user.is_superuser or (profile and profile.role == "admin")):
        return HttpResponseForbidden("Only administrators can manage announcements.")

    announcements = Announcement.objects.all().order_by('-created_at')

    return render(request, "main/announcement_list.html", {
        "announcements": announcements,
    })


@login_required
def announcement_update(request, ann_id):
    profile = getattr(request.user, "profile", None)

    if not (request.user.is_superuser or (profile and profile.role == "admin")):
        return HttpResponseForbidden("Only administrators can edit announcements.")

    announcement = get_object_or_404(Announcement, id=ann_id)

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated successfully.")
            return redirect("main:announcement_list")
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, "main/add_announcement.html", {
        "form": form,
        "page_title": "Edit Announcement",
    })


@login_required
def announcement_delete(request, ann_id):
    profile = getattr(request.user, "profile", None)

    if not (request.user.is_superuser or (profile and profile.role == "admin")):
        return HttpResponseForbidden("Only administrators can delete announcements.")

    announcement = get_object_or_404(Announcement, id=ann_id)

    if request.method == "POST":
        announcement.delete()
        messages.success(request, "Announcement deleted successfully.")
        return redirect("main:announcement_list")

    return render(request, "main/announcement_delete.html", {
        "announcement": announcement,
    })
