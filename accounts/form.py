from django import forms
from students.models import StudentProfile
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter username"}
        ),
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter password"}
        ),
    )


class StudentRegisterForm(forms.ModelForm):
    # username = forms.CharField(max_length=100)
    # password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    # email = forms.EmailField(max_length=150)
    DEPT_CHOICES = [
        ("CS", "Computer Science"),
        ("IT", "Information Technology"),
        ("ECE", "Electronics"),
        ("ME", "Mechanical"),
    ]
    roll_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Roll Number"}
        ),
    )
    department = forms.ChoiceField(
        choices=DEPT_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )
    year_of_admission = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter Year"}
        )
    )

    class Meta:

        model = User
        fields = ["username", "email", "password"]

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter email"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Enter password"}
            ),
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter email"}
            ),
        }




class EditProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["roll_number", "department", "year_of_admission", "profile_image"]

        widgets = {
            "roll_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Roll Number"}
            ),
            "department": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Department"}
            ),
            "year_of_admission": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter Year"}
            ),
            "profile_image": forms.FileInput(attrs={"class": "form-control"}),
        }
