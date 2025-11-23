from django import forms
from students.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "description"]
