from django.db import models
from django.contrib.auth.models import User
from courses.models import SchoolClass, Subject, ClassSubject


# =========================
# الدروس (Lessons)
# =========================
class Lesson(models.Model):
    class_subject = models.ForeignKey(
        ClassSubject,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lesson: {self.title} - {self.class_subject}"


# =========================
# الواجبات (Homework)
# =========================
class Homework(models.Model):
    class_subject = models.ForeignKey(
        ClassSubject,
        on_delete=models.CASCADE,
        related_name='homeworks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"HW: {self.title} ({self.class_subject})"


# =========================
# الكويز الأساسي (Quiz)
# =========================
class Quiz(models.Model):
    class_subject = models.ForeignKey(
        ClassSubject,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    title = models.CharField(max_length=200)
    total_marks = models.PositiveIntegerField(default=10)
    due_date = models.DateField(null=True, blank=True)

    # حقول إضافية لنظام الكويز
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="مدة الكويز بالدقائق (اختياري)"
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quiz: {self.title} ({self.class_subject})"


# =========================
# تسليمات الواجب (HomeworkSubmission)
# =========================
class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} submission for {self.homework.title}"


# =========================
# تسليمات الكويز النصية (QuizSubmission)
# (نخليها زي ما هي لو تحتاجها)
# =========================
class QuizSubmission(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} submission for {self.quiz.title}"


# =========================
# أسئلة الكويز (Question)
# =========================
class Question(models.Model):
    SINGLE = 'single'
    MULTI = 'multi'
    TEXT = 'text'

    QTYPE_CHOICES = [
        (SINGLE, 'اختيار واحد'),
        (MULTI, 'اختيارات متعددة'),
        (TEXT, 'إجابة نصيّة'),
    ]

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    text = models.TextField()
    qtype = models.CharField(
        max_length=10,
        choices=QTYPE_CHOICES,
        default=SINGLE
    )
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Q{self.pk} - {self.quiz.title}"


# =========================
# خيارات السؤال (Choice)
# =========================
class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.text[:30]}"


# =========================
# محاولات الطلاب (QuizAttempt)
# =========================
class QuizAttempt(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} - Attempt {self.pk}"


# =========================
# إجابات الأسئلة داخل المحاولة (Answer)
# =========================
class Answer(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    # للأسئلة الاختيارية
    selected_choices = models.ManyToManyField(
        Choice,
        blank=True
    )
    # للأسئلة النصية
    text_answer = models.TextField(blank=True)

    def __str__(self):
        return f"Answer: attempt {self.attempt.pk} - Q{self.question.pk}"
