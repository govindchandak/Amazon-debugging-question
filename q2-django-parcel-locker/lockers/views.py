import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from . import services


def _error(err):
    return JsonResponse({"error": str(err)}, status=err.status)


@csrf_exempt
@require_POST
def deposit_parcel(request):
    data = json.loads(request.body or "{}")
    try:
        parcel = services.deposit(data.get("tracking_id"), data.get("size"))
    except services.LockerError as err:
        return _error(err)
    return JsonResponse({
        "tracking_id": parcel.tracking_id,
        "locker": parcel.locker.code,
        "pickup_code": parcel.pickup_code,
    }, status=201)


@csrf_exempt
@require_POST
def pickup_parcel(request):
    data = json.loads(request.body or "{}")
    try:
        parcel = services.pickup(data.get("tracking_id"), data.get("code"))
    except services.LockerError as err:
        return _error(err)
    return JsonResponse({"tracking_id": parcel.tracking_id, "status": parcel.status})


@require_GET
def free_lockers(request):
    size = request.GET.get("size", "S")
    if size not in services.SIZE_RANK:
        return JsonResponse({"error": "Size must be S, M or L"}, status=400)
    return JsonResponse({"size": size, "free": services.free_lockers_count(size)})
