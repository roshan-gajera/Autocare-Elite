from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def staff_required(view_func):
    def wrapper(request, *args,**kwargs):
        if request.user.is_authenticated and request.user.is_staff and not request.user.is_superuser:
            return view_func(request, *args,**kwargs)
        elif request.user.is_staff and  request.user.is_superuser:
            return redirect("admin-home")
        else:
            return redirect("user_profile")
        
    return wrapper