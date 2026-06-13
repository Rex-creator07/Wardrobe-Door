from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = "Set default Site domain for django-allauth"

    def handle(self, *args, **options):
        site, _ = Site.objects.update_or_create(
            pk=1,
            defaults={
                "domain": "127.0.0.1:8000",
                "name": "The Wardrobe Door",
            },
        )
        self.stdout.write(self.style.SUCCESS(f"Site updated: {site.domain}"))
