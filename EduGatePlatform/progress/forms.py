from django import forms
from .models import Lesson, Homework, Quiz, Question, Choice


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']
        labels = {
            'title': 'Lesson title',
            'content': 'Lesson content',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
        }


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['title', 'description', 'due_date']
        labels = {
            'title': 'Homework title',
            'description': 'Description',
            'due_date': 'Due date',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }


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
            'max_attempts',
            'is_active',
        ]
        labels = {
            'title': 'Title',
            'description': 'Description',
            'total_marks': 'Total marks',
            'due_date': 'Due date',
            'start_time': 'Start time',
            'end_time': 'End time',
            'duration_minutes': 'Duration (minutes)',
            'max_attempts': 'Max attempts (0 = unlimited)',
            'is_active': 'Is active',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_attempts': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'qtype', 'points', 'order']
        labels = {
            'text': 'Question text',
            'qtype': 'Question type',
            'points': 'Points',
            'order': 'Order',
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'qtype': forms.Select(attrs={
                'class': 'form-select',
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        labels = {
            'text': 'Choice text',
            'is_correct': 'Correct answer?',
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
