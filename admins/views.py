from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from students.models import StudentProfile, Course
from accounts.form import EditProfileForm, EditUserForm, StudentRegisterForm
from .form import CourseForm
from django.core.mail import send_mail
from django.conf import settings
from accounts.decorators import admin_required
from django.contrib.auth import get_user_model

User = get_user_model()


@admin_required
@login_required
def admin_dashboard(request):
    total_students = StudentProfile.objects.count()
    total_courses = Course.objects.count()
    return render(
        request,
        "admins/admin_dashboard.html",
        {
            "total_students": total_students,
            "total_courses": total_courses,
        },
    )


# @admin_required
def manage_students(request):
    students = User.objects.filter(role="student")

    value = request.GET.get("value")
    if value:
        students = students.filter(username__icontains=value)

    return render(
        request, "admins/manage_students.html", {"students": students, "value": value}
    )


@admin_required
def view_student(request, id):
    student = User.objects.get(id=id)
    return render(request, "admins/view_students.html", {"student": student})


@admin_required
def add_student(request):
    if request.method == "GET":
        form = StudentRegisterForm()
        return render(request, "admins/add_student.html", {"form": form})
    elif request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.role = "student"
            user.save()
            roll_number = form.cleaned_data["roll_number"]
            department = form.cleaned_data["department"]
            year_of_admission = form.cleaned_data["year_of_admission"]

            userProfile = StudentProfile.objects.create(
                user=user,
                roll_number=roll_number,
                department=department,
                year_of_admission=year_of_admission,
            )
            userProfile.save()

            send_mail(
                subject="Welcome to Student Portal",
                message=f"Hello {username},\n\nYour student account has been created successfully.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )

            return redirect("manage_students")
        else:
            return render(request, "admins/add_student.html", {"form": form})


def edit_student(request, id):
    user = User.objects.get(id=id)
    profile = StudentProfile.objects.get(user=user)

    if request.method == "GET":
        user_form = EditUserForm(instance=user)
        profile_form = EditProfileForm(instance=profile)

        return render(
            request,
            "admins/edit_student.html",
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )

    elif request.method == "POST":
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.save()
            profile_form.save_m2m()

            return redirect("manage_students")

        return render(
            request,
            "admins/edit_student.html",
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )


def delete_student(request, id):
    student = User.objects.get(id=id)
    student.delete()
    return redirect("manage_students")


# next  course


def manage_courses(request):
    courses = Course.objects.all()
    return render(request, "admins/manage_course.html", {"courses": courses})


def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_courses")

        return render(request, "admins/add_course.html", {"form": form})
    else:
        form = CourseForm()

    return render(request, "admins/add_course.html", {"form": form})


def edit_course(request, id):
    course = Course.objects.get(id=id)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("manage_courses")

    else:
        form = CourseForm(instance=course)

    return render(request, "admins/edit_course.html", {"form": form})


def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect("manage_courses")


from django.shortcuts import get_object_or_404, redirect


def deactivate_student(request, id):
    user = get_object_or_404(User, id=id)
    user.studentprofile.is_active = False
    user.studentprofile.save()
    return redirect("manage_students")


def activate_student(request, id):
    user = get_object_or_404(User, id=id)
    print(user)
    user.studentprofile.is_active = True
    user.studentprofile.save()
    return redirect("manage_students")
