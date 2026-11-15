import secrets

from django.conf import settings
from django.db import models


class Student(models.Model):
    BRANCHES = ['CSE', 'IT', 'ECE', 'EEE', 'MECH', 'CIVIL', 'AIDS']

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=10)
    cgpa = models.FloatField()
    backlogs = models.PositiveIntegerField(default=0)
    skills = models.JSONField(default=list)          # [{"name": "Python", "level": 4}, ...]  level 1-5
    test_scores = models.JSONField(default=list)     # mock test percentages, e.g. [70, 75]
    target_ctcs = models.JSONField(default=list)     # dream packages as text, e.g. ["12.5", "9"]

    def __str__(self):
        return f'{self.roll_no} {self.name}'


class AuthToken(models.Model):
    key = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tokens')
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def issue(cls, user):
        return cls.objects.create(key=secrets.token_hex(20), user=user)
