from django.core.management.base import BaseCommand

from wishlist.models import Product


class Command(BaseCommand):
    help = "Add sample products so you can try the app in a browser."

    def handle(self, *args, **options):
        for name, price in [("Echo Dot", 4499), ("Kindle", 9999), ("Fire TV Stick", 3999)]:
            Product.objects.get_or_create(name=name, defaults={"price": price})
        self.stdout.write(self.style.SUCCESS("Sample products added."))
