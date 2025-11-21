from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from students.models import StudentProfile




@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        messages.error(request, "Admins only.")
        return redirect("login")

    return render(request, "admins/admin_dashboard.html")


# get_user_model
# this is because
User = get_user_model()


def manage_students(request):
    students = User.objects.filter(role="student")
    return render(request, "admins/manage_students.html", {"students": students})


def view_student(request, id):
    student = User.objects.get(id=id)
    return render(request, "admins/view_student.html", {"student": student})


def edit_student(request, id):
    student = User.objects.get(id=id)
    profile = StudentProfile.objects.get(user=student)
    if request.method == "POST":
        student.username = request.POST.get("username")
        student.email = request.POST.get("email")
        student.save()

        profile.department = request.POST.get("department")
        profile.year = request.POST.get("year")
        profile.save()
        return redirect("view_student", id=student.id)

    return render(
        request,
        "admins/edit_student.html",
        {
            "student": student,
            "profile": profile,
        },
    )

def delete_student(request, id):
    student=User.objects.get(id=id)
    student.delete()
    return redirect("manage_students")
