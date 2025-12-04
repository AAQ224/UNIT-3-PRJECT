from django.contrib import admin
from .models import (Lesson,
    Homework, Quiz,
    HomeworkSubmission,
    QuizSubmission,
    Question,
    Choice,
    QuizAttempt,
    Answer,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_subject', 'is_active', 'due_date', 'start_time', 'end_time')
    list_filter = ('class_subject', 'is_active')
    search_fields = ('title',)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'qtype', 'points', 'order')
    list_filter = ('quiz', 'qtype')
    inlines = [ChoiceInline]


admin.site.register(Lesson)
admin.site.register(Homework)
admin.site.register(HomeworkSubmission)
admin.site.register(QuizSubmission)
admin.site.register(Choice)
admin.site.register(QuizAttempt)
admin.site.register(Answer)
