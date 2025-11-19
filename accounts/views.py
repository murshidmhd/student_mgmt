from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from students.models import StudentProfile

User = get_user_model()


def register_student(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        roll_number = request.POST.get("roll_number")
        department = request.POST.get("department")
        year = request.POST.get("year")

        # Basic validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register_student")

        if not year.isdigit():
            messages.error(request, "Year must be a number.")
            return redirect("register_student")

        year = int(year)

        user = User.objects.create_user(
            username=username, password=password, role="student"
        )

        StudentProfile.objects.create(
            user=user,
            roll_number=roll_number,
            department=department,
            year_of_admission=year,
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "register_student.html")


from django.contrib.auth import authenticate, login
from django.contrib import messages


from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

        login(request, user)
        messages.success(request, "Login successful!")

        if user.role == "admin":
            return redirect("admin_dashboard")
        else:
            return redirect("student_dashboard")

    return render(request, "login.html")


# @login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        messages.error(request, "Access denied.")
        return redirect("student_dashboard")

    return render(request, "admin_dashboard.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")
