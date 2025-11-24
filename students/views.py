from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from django.contrib import messages


@login_required
def student_dashboard(request):
    messages.success(request, "Welcome to your dashboard!")
    return render(request, "student_dashboard.html")


@login_required
def student_profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    return render(request, "student_profile.html", {"profile": profile})


@login_required
def edit_profile(request):
    profile = StudentProfile.objects.get(user=request.user)

    if request.method == "POST":
        profile.roll_number = request.POST.get("roll_number")
        profile.department = request.POST.get("department")
        profile.year_of_admission = request.POST.get("year")

        if "profile_image" in request.FILES:
            profile.profile_image = request.FILES["profile_image"]

        profile.save()

        return redirect("student_profile")
    return render(request, "edit_profile.html", {"profile": profile})


def my_course(request):
    student = StudentProfile.objects.get(user=request.user)
    course = student.courses.all()
    return render(request, "my_course.html", {"courses": course})
