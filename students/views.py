from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from accounts.decorators import student_required


@login_required
@student_required
def student_dashboard(request):
    return render(request, "student_dashboard.html")


@login_required
@student_required
def student_profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    return render(request, "student_profile.html", {"profile": profile})
