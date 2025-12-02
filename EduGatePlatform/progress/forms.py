from django import forms
from .models import Lesson, Homework, Quiz


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
        fields = ['title', 'total_marks', 'due_date']  
