from django.conf import settings
from django.db import models


class Company(models.Model):
    TIERS = [('DREAM', 'Dream'), ('CORE', 'Core'), ('MASS', 'Mass recruiter')]

    name = models.CharField(max_length=100, unique=True)
    tier = models.CharField(max_length=10, choices=TIERS, default='CORE')
    ctc_lpa = models.FloatField()

    def __str__(self):
        return self.name


class Drive(models.Model):
    OPEN, CLOSED = 'OPEN', 'CLOSED'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='drives')
    role = models.CharField(max_length=100)
    branches = models.JSONField(default=list)          # e.g. ["CSE", "IT"]
    min_cgpa = models.FloatField(default=0)
    max_backlogs = models.PositiveIntegerField(default=0)
    required_skills = models.JSONField(default=list)   # e.g. ["Python", "SQL"]
    seats = models.PositiveIntegerField(default=10)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=10, default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['deadline', 'id']

    def __str__(self):
        return f'{self.company.name} – {self.role}'


class SavedDrive(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    drive = models.ForeignKey(Drive, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'drive')


class DriveNote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    drive = models.ForeignKey(Drive, on_delete=models.CASCADE, related_name='notes')
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
