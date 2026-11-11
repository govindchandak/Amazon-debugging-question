from django.core.management.base import BaseCommand

from lockers.models import Locker


class Command(BaseCommand):
    help = "Add sample lockers so you can try the API."

    def handle(self, *args, **options):
        for code, size in [("A1", "S"), ("A2", "S"), ("B1", "M"), ("C1", "L")]:
            Locker.objects.get_or_create(code=code, defaults={"size": size})
        self.stdout.write(self.style.SUCCESS("Sample lockers added."))
