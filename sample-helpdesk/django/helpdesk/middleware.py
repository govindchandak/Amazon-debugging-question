from django.http import JsonResponse

from .users import USERS, User


class RequireUserMiddleware:
    """Every /api request must say who is calling, in the X-User header."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            name = request.headers.get("X-User")
            if name and name not in USERS:
                return JsonResponse({"error": "Unknown user"}, status=401)
            request.app_user = User(name, USERS.get(name))
        return self.get_response(request)
