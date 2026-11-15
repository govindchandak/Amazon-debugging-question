"""Mission 3 – the apply service used by the view."""
from django.utils import timezone

from drives.models import Drive
from drives.rules import profile_reasons

from .models import Application


class ApplyError(Exception):
    def __init__(self, code, message, status):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


def apply_to_drive(student, drive):
    """Create an application. Returns the new Application, or raises ApplyError."""
    if drive.status != Drive.OPEN or timezone.now() >= drive.deadline:
        raise ApplyError('DRIVE_CLOSED', 'Applications for this drive are closed', 409)
    if Application.objects.filter(student=student, drive=drive, status=Application.APPLIED).exists():
        raise ApplyError('ALREADY_APPLIED', 'You have already applied to this drive', 400)
    reasons = profile_reasons(student, drive)
    if reasons:
        raise ApplyError('NOT_ELIGIBLE', reasons[0], 422)
    application = Application.objects.get_or_create(student=student, drive=drive, status=Application.APPLIED)
    return application
