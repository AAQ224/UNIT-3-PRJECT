from django import forms
from django.contrib.auth.models import User
from .models import SchoolClass, Subject, ClassSubject, StudentClassEnrollment
from accounts.models import Profile


class ClassSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassSubject
        fields = ["school_class", "subject", "teacher", "academic_year"]
        widgets = {
            "school_class": forms.Select(attrs={"class": "form-select"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "teacher": forms.Select(attrs={"class": "form-select"}),
            "academic_year": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        teacher_ids = Profile.objects.filter(role="teacher").values_list("user_id", flat=True)
        self.fields["teacher"].queryset = User.objects.filter(id__in=teacher_ids)


class StudentMultiEnrollmentForm(forms.Form):
    school_class = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(profile__role="student"),
        widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        student_ids = Profile.objects.filter(role='student').values_list('user_id', flat=True)
        qs = User.objects.filter(id__in=student_ids)

        self.fields['students'].queryset = qs
        self.fields['students'].label_from_instance = (
    lambda obj: f"{obj.profile.full_name} (ID: {obj.id})"
)

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "code", "description"]  
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            'code': forms.TextInput(attrs={'class': 'form-control'}), # تطبيق Bootstrap
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
