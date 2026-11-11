import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from . import services
from .errors import HttpError, api


def body(request):
    return json.loads(request.body or "{}")


@csrf_exempt
@require_http_methods(["GET", "POST"])
@api
def tickets(request):
    if request.method == "POST":
        data = body(request)
        title = data.get("title")
        if title is None:
            raise HttpError(400, "Title is required")
        ticket = services.create_ticket(title.strip(), data.get("description", ""), request.app_user)
        return JsonResponse(ticket, status=201)

    page = int(request.GET.get("page", 1))
    return JsonResponse(services.list_tickets(request.app_user, page), safe=False)


@require_http_methods(["GET"])
@api
def ticket_detail(request, ticket_id):
    return JsonResponse(services.get_ticket(ticket_id, request.app_user))


@csrf_exempt
@require_http_methods(["POST"])
@api
def replies(request, ticket_id):
    reply = services.add_reply(ticket_id, body(request).get("message"), request.app_user)
    return JsonResponse(reply, status=201)


@csrf_exempt
@require_http_methods(["PATCH"])
@api
def ticket_status(request, ticket_id):
    ticket = services.change_status(ticket_id, body(request).get("status"), request.app_user)
    return JsonResponse(ticket)


@require_http_methods(["GET"])
@api
def notification_count(request):
    return JsonResponse({"count": services.count_replies_from_others(request.app_user)})
