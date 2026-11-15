from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import AuthToken, Student
from applications.models import Application
from drives.models import Company, Drive


class Command(BaseCommand):
    help = 'Reset the database and load demo students, companies and drives.'

    def handle(self, *args, **options):
        for model in (Application, Drive, Company, AuthToken, Student):
            model.objects.all().delete()
        User.objects.all().delete()
        now = timezone.now()

        tpo = User.objects.create_user('tpo@college.edu', 'tpo@college.edu', 'Password@123', is_staff=True)
        students = [
            ('sam.rivera@email.com', 'Sam Rivera', '21CS001', 'CSE', 8.4, 0, [{'name': 'Python', 'level': 4}, {'name': 'SQL', 'level': 3}, {'name': 'Django', 'level': 3}], [72, 81], ['12.5', '9', '45']),
            ('priya.nair@email.com', 'Priya Nair', '21IT014', 'IT', 7.6, 1, [{'name': 'Java', 'level': 4}, {'name': 'Spring Boot', 'level': 3}], [65, 70], ['8']),
        ]
        for email, name, roll, branch, cgpa, backlogs, skills, scores, ctcs in students:
            user = User.objects.create_user(email, email, 'Password@123')
            Student.objects.create(user=user, name=name, roll_no=roll, branch=branch, cgpa=cgpa, backlogs=backlogs,
                                   skills=skills, test_scores=scores, target_ctcs=ctcs)

        amz = Company.objects.create(name='Amazon', tier='DREAM', ctc_lpa=44.0)
        tcs = Company.objects.create(name='TCS Digital', tier='MASS', ctc_lpa=7.0)
        zoho = Company.objects.create(name='Zoho', tier='CORE', ctc_lpa=8.4)
        Drive.objects.create(company=amz, role='SDE I', branches=['CSE', 'IT', 'ECE'], min_cgpa=7.0, max_backlogs=0,
                             required_skills=['Python', 'Data Structures', 'SQL'], seats=5, deadline=now + timedelta(days=3))
        Drive.objects.create(company=tcs, role='Digital Engineer', branches=['CSE', 'IT', 'ECE', 'EEE', 'MECH'], min_cgpa=6.0,
                             max_backlogs=1, required_skills=['Java', 'SQL'], seats=50, deadline=now + timedelta(days=5))
        Drive.objects.create(company=zoho, role='Member Technical Staff', branches=['CSE', 'IT'], min_cgpa=6.5, max_backlogs=0,
                             required_skills=['Java', 'Problem Solving'], seats=8, deadline=now + timedelta(days=2))
        self.stdout.write(self.style.SUCCESS(f'Seeded {Student.objects.count()} students, {tpo.username} (TPO) and {Drive.objects.count()} drives.'))
