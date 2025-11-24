from django.shortcuts import render, redirect
from students.models import StudentProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.models import User
from accounts.form import LoginForm, StudentRegisterForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def register_student(request):
    form = StudentRegisterForm()
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            roll_number = form.cleaned_data["roll_number"]
            department = form.cleaned_data["department"]
            year = form.cleaned_data["year_of_admission"]

            user = User(username=username, email=email, role="student")
            user.set_password(password)
            user.save()

            # manager object
            StudentProfile.objects.create(
                user=user,
                roll_number=roll_number,
                department=department,
                year_of_admission=year,
            )

            send_mail(
                subject="Welcome to Student Portal",
                message=f"Hello {username},\n\nYour student account has been created successfully.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )

            return redirect("login")

    return render(request, "register_student.html", {"form": form})


def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.error(request, "Invalid username or password")
                return render(request, "login.html", {"form": form})
            else:
                login(request, user)

                if user.role == "admin":
                    return redirect("admin_dashboard")
                else:
                    return redirect("student_dashboard")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


