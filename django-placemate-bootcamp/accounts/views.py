import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .middleware import login_required_api
from .models import AuthToken, Student
from .summary import build_summary


@csrf_exempt
@require_http_methods(['POST'])
def login(request):
    try:
        data = json.loads(request.body or b'{}')
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    user = authenticate(username=(data.get('email') or '').lower(), password=data.get('password') or '')
    if user is None:
        return JsonResponse({'error': 'Invalid email or password'}, status=401)
    return JsonResponse({'token': AuthToken.issue(user).key, 'isTpo': user.is_staff})


@require_http_methods(['GET'])
@login_required_api
def my_summary(request):
    student = Student.objects.filter(user=request.api_user).first()
    if student is None:
        return JsonResponse({'error': 'Student profile not found'}, status=404)
    return JsonResponse({'summary': build_summary(student)})
