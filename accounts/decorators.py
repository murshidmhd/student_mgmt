from django.shortcuts import redirect
from django.contrib import messages

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != "student":
            messages.error(request, "Access denied. Students only.")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper
