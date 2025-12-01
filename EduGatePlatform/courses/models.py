from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SchoolClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    grade_level = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Grade {self.grade_level})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class ClassSubject(models.Model):
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='class_subjects'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='class_subjects'
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teaching_subjects'
    )
    academic_year = models.CharField(max_length=20, default="2025-2026")

    class Meta:
        unique_together = ('school_class', 'subject', 'teacher', 'academic_year')

    def __str__(self):
        return f"{self.school_class} - {self.subject} - {self.teacher.username}"


class StudentClassEnrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='class_enrollments'
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='students'
    )
    academic_year = models.CharField(max_length=20, default="2025-2026")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'school_class', 'academic_year')

    def __str__(self):
        return f"{self.student.username} in {self.school_class} ({self.academic_year})"
