"""Bearer-token authentication. Sets request.api_user (or None)."""
from functools import wraps

from django.http import JsonResponse

from .models import AuthToken


def token_auth_middleware(get_response):
    def middleware(request):
        request.api_user = None
        header = request.headers.get('Authorization', '')
        if header.startswith('Bearer '):
            token = AuthToken.objects.select_related('user').filter(key=header[7:].strip()).first()
            if token:
                request.api_user = token.user
        return get_response(request)
    return middleware


def login_required_api(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.api_user is None:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return view(request, *args, **kwargs)
    return wrapper


def tpo_required(view):
    """Only placement-office staff (is_staff users) may call the view."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.api_user is None:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        if not request.api_user.is_staff:
            return JsonResponse({'error': 'Only the placement office can do this'}, status=403)
        return view(request, *args, **kwargs)
    return wrapper
