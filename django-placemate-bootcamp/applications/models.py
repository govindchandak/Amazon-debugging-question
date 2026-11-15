from django.db import models

from accounts.models import Student
from drives.models import Drive


class Application(models.Model):
    APPLIED, WITHDRAWN, SHORTLISTED = 'APPLIED', 'WITHDRAWN', 'SHORTLISTED'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    drive = models.ForeignKey(Drive, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=12, default=APPLIED)
    test_score = models.FloatField(null=True, blank=True)   # company online-test %, filled in by the TPO
    applied_at = models.DateTimeField(auto_now_add=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)
