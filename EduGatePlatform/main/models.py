from django.db import models

# Create your models here.

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('trip', 'Trip'),
        ('party', 'Party'),
        ('holiday', 'Holiday'),
        ('exam', 'Exam'),
        ('general', 'General'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="announcements/", blank=True, null=True)

    def __str__(self):
        return self.title
