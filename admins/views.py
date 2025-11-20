from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        messages.error(request, "Admins only.")
        return redirect("login")

    return render(request, "admin_dashboard.html")
