import functools

from django.http import JsonResponse


class HttpError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


def api(view):
    """Turns HttpError into a JSON response with the right status code."""

    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except HttpError as err:
            return JsonResponse({"error": str(err)}, status=err.status)

    return wrapper
