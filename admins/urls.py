from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("students/", views.manage_students, name="manage_students"),
    path("students/<int:id>/", views.view_student, name="view_student"),
    path("students/<int:id>/edit/", views.edit_student, name="edit_student"),
    path("students/<int:id>/delete/", views.delete_student, name="delete_student"),
    path("students/add", views.add_student, name="add_student"),
    # course
    path("courses/", views.manage_courses, name="manage_courses"),
    path("courses/add", views.add_course, name="add_course"),
    path("courses/<int:id>/edit", views.edit_course, name="edit_course"),
    path("courses/<int:id>/delete", views.delete_course, name="delete_course"),
]
