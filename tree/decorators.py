from functools import wraps

from django.http import HttpResponse

  
def staff_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_staff:
                return HttpResponse("you are not allowed to access this page !")
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator