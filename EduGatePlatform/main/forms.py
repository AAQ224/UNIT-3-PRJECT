from django import forms
from courses.models import SchoolClass
from main.models import Announcement

class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ["name", "grade_level"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "grade_level": forms.NumberInput(attrs={"class": "form-control"}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "category", "content", "is_important", "start_date", "end_date", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_important": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
