import json

from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from accounts.middleware import login_required_api, tpo_required
from accounts.models import Student

from .models import Drive, DriveNote, SavedDrive
from .rules import profile_reasons
from .serializers import serialize_drive


# ---------------------------------------------------------------------------
# Mission 2 – request lifecycle (URLs, methods, request body, JSON response)
# ---------------------------------------------------------------------------

@require_http_methods(['GET'])
def list_drives(request):
    """GET /api/drives/ -> JSON array of OPEN drives, earliest deadline first."""
    drives = Drive.objects.select_related('company').filter(status=Drive.OPEN)
    return JsonResponse([serialize_drive(d) for d in drives])


@require_http_methods(['GET'])
def drive_detail(request, drive_id):
    drive = Drive.objects.select_related('company').filter(id=drive_id).first()
    if drive is None:
        return JsonResponse({'error': 'Drive not found'}, status=404)
    data = serialize_drive(drive)
    data['notes'] = drive.notes.count()
    return JsonResponse({'drive': data})


@csrf_exempt
@require_http_methods(['POST'])
@login_required_api
def save_drive(request, drive_id):
    """POST bookmarks a drive (201), DELETE removes the bookmark (200)."""
    drive = Drive.objects.filter(id=drive_id).first()
    if drive is None:
        return JsonResponse({'error': 'Drive not found'}, status=404)
    if request.method == 'DELETE':
        deleted, _ = SavedDrive.objects.filter(user=request.api_user, drive=drive).delete()
        if not deleted:
            return JsonResponse({'error': 'Drive is not saved'}, status=404)
        return JsonResponse({'message': 'Drive removed from saved list'})
    _, created = SavedDrive.objects.get_or_create(user=request.api_user, drive=drive)
    return JsonResponse({'message': 'Drive saved' if created else 'Drive already saved'}, status=201 if created else 200)


@csrf_exempt
@require_http_methods(['POST'])
@login_required_api
def add_note(request, drive_id):
    """POST /api/drives/<id>/notes with a JSON body {"note": "..."}."""
    drive = Drive.objects.filter(id=drive_id).first()
    if drive is None:
        return JsonResponse({'error': 'Drive not found'}, status=404)
    text = (request.POST.get('note') or '').strip()
    if not text:
        return JsonResponse({'error': 'note is required'}, status=400)
    note = DriveNote.objects.create(user=request.api_user, drive=drive, text=text[:300])
    return JsonResponse({'message': 'Note added', 'note': {'_id': str(note.id), 'text': note.text}}, status=201)


# ---------------------------------------------------------------------------
# Mission 4 – Django ORM
# ---------------------------------------------------------------------------

@require_http_methods(['GET'])
def search_drives(request):
    """GET /api/drives/search?skill=python&minCtc=10 (both optional)."""
    drives = Drive.objects.select_related('company').filter(status=Drive.OPEN)
    min_ctc = request.GET.get('minCtc')
    if min_ctc:
        try:
            drives = drives.filter(company__ctc_lpa__gt=float(min_ctc))
        except ValueError:
            return JsonResponse({'error': 'minCtc must be a number'}, status=400)
    skill = (request.GET.get('skill') or '').strip().lower()
    results = [d for d in drives if not skill or skill in [s.lower() for s in d.required_skills]]
    return JsonResponse({'count': len(results), 'drives': [serialize_drive(d) for d in results]})


@require_http_methods(['GET'])
def drive_stats(request):
    """GET /api/drives/stats -> active (APPLIED) applications per drive."""
    drives = (
        Drive.objects.select_related('company')
        .annotate(active_applications=Count('applications'))
        .order_by('id')
    )
    return JsonResponse({'stats': [
        {'_id': str(d.id), 'company': d.company.name, 'role': d.role, 'activeApplications': d.active_applications}
        for d in drives
    ]})


# ---------------------------------------------------------------------------
# Mission 5 – authentication and business logic
# ---------------------------------------------------------------------------

@require_http_methods(['GET'])
def eligibility(request, drive_id):
    """GET /api/drives/<id>/eligibility for the logged-in student."""
    drive = Drive.objects.select_related('company').filter(id=drive_id).first()
    if drive is None:
        return JsonResponse({'error': 'Drive not found'}, status=404)
    student = Student.objects.get(user=request.api_user)
    reasons = profile_reasons(student, drive)
    if drive.status != Drive.OPEN or timezone.now() >= drive.deadline:
        reasons.append('Applications for this drive are closed')
    return JsonResponse({'driveId': str(drive.id), 'eligible': not reasons, 'reasons': reasons})


@csrf_exempt
@require_http_methods(['POST'])
@login_required_api
def close_drive(request, drive_id):
    """POST /api/drives/<id>/close – placement office only."""
    drive = Drive.objects.filter(id=drive_id).first()
    if drive is None:
        return JsonResponse({'error': 'Drive not found'}, status=404)
    if drive.status == Drive.CLOSED:
        return JsonResponse({'error': 'Drive is already closed'}, status=409)
    drive.status = Drive.CLOSED
    drive.save()
    return JsonResponse({'message': 'Drive closed', 'drive': serialize_drive(drive)})
