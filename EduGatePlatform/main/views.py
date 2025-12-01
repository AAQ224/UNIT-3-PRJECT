from django.shortcuts import render
from .models import Announcement
from django.utils import timezone

# Create your views here.

def home(request):
    today = timezone.now().date()
    announcements = Announcement.objects.filter(
        models.Q(start_date__isnull=True) | (models.Q(start_date__lte=today)),
        models.Q(end_date__isnull=True) | (models.Q(end_date__gte=today))
    ).order_by('-is_important', '-created_at')[:6]  # أهم 6 إعلانات

    context = {
        'announcements': announcements,
    }
    return render(request, 'main/home.html', context)