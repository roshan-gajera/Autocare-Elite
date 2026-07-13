from django.shortcuts import redirect


def super_required(view_func):
    def wrapper(request, *args,**kwargs):
        if request.user.is_authenticated and request.user.is_superuser and request.user.is_staff:
            return view_func(request, *args,**kwargs)
        elif not request.user.is_superuser and request.user.is_staff:
            return redirect("servicesite-profile")
        else:
            return redirect("user_profile")
        
    return wrapper