from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from accounts.middleware import login_required_api, tpo_required
from accounts.models import Student
from drives.models import Drive
from drives.rules import profile_reasons

from .models import Application
from .serializers import serialize_application
from .services import ApplyError, apply_to_drive


def _student_or_404(request):
    return Student.objects.filter(user=request.api_user).first()


# ---------------------------------------------------------------------------
# Mission 3 – views and services (status codes, error contract, response shape)
# ---------------------------------------------------------------------------

@csrf_exempt
@require_http_methods(['POST'])
@login_required_api
def apply(request, drive_id):
    """POST /api/drives/<id>/apply"""
    student = _student_or_404(request)
    drive = Drive.objects.select_related('company').filter(id=drive_id).first()
    if student is None or drive is None:
        return JsonResponse({'error': 'NOT_FOUND', 'message': 'Student or drive not found'}, status=404)
    try:
        application = apply_to_drive(student, drive)
    except ApplyError as err:
        return JsonResponse({'error': err.code, 'message': err.message}, status=err.status)
    return JsonResponse({'message': 'Application submitted', 'application': serialize_application(application)})


@require_http_methods(['GET'])
@login_required_api
def my_applications(request):
    """GET /api/applications/me – newest first (Mission 4 checks the ordering)."""
    student = _student_or_404(request)
    if student is None:
        return JsonResponse({'error': 'NOT_FOUND', 'message': 'Student not found'}, status=404)
    applications = (
        Application.objects.select_related('drive__company')
        .filter(student=student)
        .order_by('applied_at', 'id')
    )
    return JsonResponse({'applications': [serialize_application(a) for a in applications]})


# ---------------------------------------------------------------------------
# Mission 4 – Django ORM
# ---------------------------------------------------------------------------

@require_http_methods(['GET'])
@login_required_api
def application_detail(request, application_id):
    application = (
        Application.objects.select_related('drive__company', 'student')
        .get(id=application_id, student__user=request.api_user)
    )
    if application is None:
        return JsonResponse({'error': 'NOT_FOUND', 'message': 'Application not found'}, status=404)
    return JsonResponse({'application': serialize_application(application)})


@csrf_exempt
@require_http_methods(['POST'])
@login_required_api
def withdraw(request, application_id):
    application = (
        Application.objects.select_related('drive__company')
        .filter(id=application_id, student__user=request.api_user)
        .first()
    )
    if application is None:
        return JsonResponse({'error': 'NOT_FOUND', 'message': 'Application not found'}, status=404)
    if application.status != Application.APPLIED:
        return JsonResponse({'error': 'INVALID_STATE', 'message': 'Only active applications can be withdrawn'}, status=409)
    application.status = Application.WITHDRAWN
    application.withdrawn_at = timezone.now()
    return JsonResponse({'message': 'Application withdrawn', 'application': serialize_application(application)})


# ---------------------------------------------------------------------------
# Mission 6 – practical challenge: the drive shortlist (Amazon-size feature)
# ---------------------------------------------------------------------------

def _build_shortlist(drive):
    """Rank eligible applicants. See README, Mission 6, for every rule."""
    applications = (
        Application.objects.select_related('student')
        .filter(drive=drive)
        .order_by('id')
    )
    required = [s.strip().lower() for s in drive.required_skills]

    candidates = []
    for application in applications:
        student = application.student

        # 1. profile must still meet the drive criteria
        if profile_reasons(student, drive):
            continue

        # 2. students without a test score cannot be ranked yet
        if application.test_score is None:
            continue

        # 3. skill match against the drive's required skills
        student_skills = {s['name'].strip() for s in student.skills}
        matched = [skill for skill in drive.required_skills if skill.strip() in student_skills]
        skill_match = len(matched) / len(required) if required else 1.0

        # 4. weighted score
        cgpa_part = (student.cgpa / 10) * 0.4
        test_part = (application.test_score / 100) * 0.4
        skill_part = skill_match * 0.2
        score = cgpa_part + test_part + skill_part

        candidates.append({
            'application': application,
            'student': student,
            'score': score,
            'matched': matched,
        })

    # 5. order: score high -> low, then CGPA high -> low, then roll number A -> Z
    candidates.sort(key=lambda c: (c['score'], c['student'].cgpa, c['student'].roll_no), reverse=True)

    # 6. only as many students as the drive has seats
    selected = candidates[:drive.seats - 1]
    return selected, len(candidates)


@require_http_methods(['GET'])
@tpo_required
def shortlist(request, drive_id):
    """GET /api/drives/<id>/shortlist – placement office only."""
    try:
        drive = Drive.objects.select_related('company').filter(id=drive_id).first()
        if drive is None:
            return JsonResponse({'error': 'NOT_FOUND', 'message': 'Drive not found'}, status=404)

        selected, eligible_count = _build_shortlist(drive)

        if not selected:
            return JsonResponse({'message': 'No eligible applicants yet', 'shortlist': []})

        rows = []
        for rank, item in enumerate(selected, start=1):
            student = item['student']
            rows.append({
                'rank': rank,
                'applicationId': str(item['application'].id),
                'studentId': str(student.id),
                'name': student.name,
                'rollNo': student.roll_no,
                'score': round(item['score'], 3),
                'matchedSkills': item['matched'],
            })

        return JsonResponse({
            'message': f'Shortlisted {len(rows)} of {eligible_count} eligible applicants',
            'results': rows,
        })
    except Exception as exc:  # noqa: BLE001
        print(f'Shortlist error: {exc}')
        return JsonResponse({'error': 'SERVER_ERROR', 'message': 'Could not build the shortlist'}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
@tpo_required
def confirm_shortlist(request, drive_id):
    """POST /api/drives/<id>/shortlist/confirm – marks the selected applications SHORTLISTED."""
    drive = Drive.objects.select_related('company').filter(id=drive_id).first()
    if drive is None:
        return JsonResponse({'error': 'NOT_FOUND', 'message': 'Drive not found'}, status=404)
    selected, _ = _build_shortlist(drive)
    for item in selected:
        application = item['application']
        application.status = Application.SHORTLISTED
    return JsonResponse({'message': f'{len(selected)} applications shortlisted', 'count': len(selected)})
