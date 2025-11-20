from django.urls import path
from . import views

urlpatterns = [
    path("register/student/", views.register_student, name="register_student"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
