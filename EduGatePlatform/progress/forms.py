from django import forms
from .models import Lesson, Homework, Quiz, Question, Choice


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['title', 'description', 'due_date']


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            'title',
            'description',
            'total_marks',
            'due_date',
            'start_time',
            'end_time',
            'duration_minutes',
            'is_active',
        ]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'qtype', 'points', 'order']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
