from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps


def owner_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, "profile") or request.user.profile.role != "OWNER":
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def customer_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, "profile") or request.user.profile.role != "CUSTOMER":
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper