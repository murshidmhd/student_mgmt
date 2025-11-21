from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("students/", views.manage_students, name="manage_students"),
    path("students/<int:id>/", views.view_student, name="view_student"),
    path("students/<int:id>/edit/", views.edit_student, name="edit_student"),
    path("students/<int:id>/delete/", views.delete_student, name="delete_student"),
]
