from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from students.models import StudentProfile, Course
from accounts.form import EditProfileForm, EditUserForm, StudentRegisterForm
from .form import CourseForm


@login_required
def admin_dashboard(request):
    if request.user.role == "admin":
        return render(request, "admins/admin_dashboard.html")

    return redirect("login")


def manage_students(request):
    students = User.objects.filter(role="student")
    return render(request, "admins/manage_students.html", {"students": students})


def view_student(request, id):
    student = User.objects.get(id=id)
    return render(request, "admins/view_students.html", {"student": student})


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
            return redirect("manage_students")


def edit_student(request, id):
    user = User.objects.get(id=id)
    profile, created = StudentProfile.objects.get_or_create(user=user)

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
            profile_form.save()
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
        name = request.POST["name"]
        description = request.POST["description"]

        Course.objects.create(name=name, description=description)
        return redirect("manage_courses")
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
