from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
            return view_func(request, *args ,**kwargs)
        
        else:
            return redirect("servicesite-profile")
        
    return wrapper