import json
import os
import sys
from datetime import timedelta
from pathlib import Path

import django
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placemate.settings')
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from django.test import Client  # noqa: E402
from django.utils import timezone  # noqa: E402

from accounts.models import AuthToken, Student  # noqa: E402
from drives.models import Company, Drive  # noqa: E402


class Api:
    """Test client that sends JSON and (optionally) a bearer token."""

    def __init__(self, token=None):
        self.client = Client()
        self.token = token

    def _h(self):
        return {'HTTP_AUTHORIZATION': f'Bearer {self.token}'} if self.token else {}

    def get(self, path):
        return self.client.get(path, **self._h())

    def post(self, path, data=None):
        return self.client.post(path, data=json.dumps(data or {}), content_type='application/json', **self._h())

    def delete(self, path):
        return self.client.delete(path, **self._h())


@pytest.fixture
def anonymous(db):
    return Api()


@pytest.fixture
def make_student(db):
    """make_student(roll, branch='CSE', cgpa=8.0, ...) -> (Api, Student)"""
    def _make(roll, name=None, branch='CSE', cgpa=8.0, backlogs=0, skills=None, test_scores=None, target_ctcs=None):
        email = f'{roll.lower()}@college.edu'
        user = User.objects.create_user(email, email, 'Password@123')
        student = Student.objects.create(
            user=user, name=name or f'Student {roll}', roll_no=roll, branch=branch, cgpa=cgpa, backlogs=backlogs,
            skills=skills or [], test_scores=test_scores or [], target_ctcs=target_ctcs or [],
        )
        return Api(AuthToken.issue(user).key), student
    return _make


@pytest.fixture
def tpo(db):
    user = User.objects.create_user('tpo@college.edu', 'tpo@college.edu', 'Password@123', is_staff=True)
    return Api(AuthToken.issue(user).key)


@pytest.fixture
def make_drive(db):
    def _make(company='Acme', ctc=10.0, tier='CORE', role='SDE', branches=None, min_cgpa=6.0, max_backlogs=2,
              skills=None, seats=10, days_left=5, status='OPEN'):
        comp, _ = Company.objects.get_or_create(name=company, defaults={'ctc_lpa': ctc, 'tier': tier})
        return Drive.objects.create(
            company=comp, role=role, branches=branches or ['CSE', 'IT'], min_cgpa=min_cgpa, max_backlogs=max_backlogs,
            required_skills=skills or [], seats=seats, deadline=timezone.now() + timedelta(days=days_left), status=status,
        )
    return _make


@pytest.fixture
def make_application(db):
    """Create an application straight in the database (no API call)."""
    from applications.models import Application

    def _make(student, drive, test_score=None, status='APPLIED'):
        return Application.objects.create(student=student, drive=drive, test_score=test_score, status=status)
    return _make
