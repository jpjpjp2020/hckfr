from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from functools import wraps


def role_required(*roles, redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                login_url = reverse(redirect_url) if redirect_url else '/'
                return HttpResponseRedirect(login_url)
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("No permission to access this page.")
        return _wrapped_view
    return decorator