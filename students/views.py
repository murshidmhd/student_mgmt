from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from accounts.decorators import student_required
from django.contrib import messages


@login_required
# @student_required
def student_dashboard(request):
    return render(request, "student_dashboard.html")


@login_required
# @student_required
def student_profile(request):

    # we do in here is we just
    # after login in here we only get the name
    # so we look to the student profile and that obect we get the profile all data with user name
    profile = StudentProfile.objects.get(user=request.user)
    return render(request, "student_profile.html", {"profile": profile})


@login_required
@student_required
def edit_profile(request):
    profile = StudentProfile.objects.get(user=request.user)

    if request.method == "POST":
        profile.roll_number = request.POST.get("roll_number")
        profile.department = request.POST.get("department")
        profile.year_of_admission = request.POST.get("year")

        if "profile_image" in request.FILES:
            profile.profile_image = request.FILES["profile_image"]

        profile.save()

        messages.success(request, "profile updated successfully!")
        return redirect("student_profile")
    return render(request, "edit_profile.html", {"profile": profile})
