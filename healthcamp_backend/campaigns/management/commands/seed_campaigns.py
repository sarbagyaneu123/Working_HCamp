from django.core.management.base import BaseCommand
from campaigns.models import Campaign
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Seed sample health campaigns"

    def handle(self, *args, **options):
        samples = [
            dict(
                title="Vaccination Drive",
                description="Free COVID-19 and Influenza vaccination for all.",
                location="Community Health Center, Ward 5",
                date=date.today() + timedelta(days=7),
                helpline_number="+977-9800000000",
                type="vaccination",
                image_url="https://example.com/vax.jpg",
            ),
            dict(
                title="Free Health Checkup",
                description="General health checkup: BP, sugar, BMI, and consultation.",
                location="City Hall",
                date=date.today() + timedelta(days=14),
                helpline_number="+977-9811111111",
                type="checkup",
                image_url="https://example.com/checkup.jpg",
            ),
        ]

        created = 0
        for data in samples:
            obj, was_created = Campaign.objects.get_or_create(
                title=data["title"], defaults=data
            )
            created += 1 if was_created else 0
        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} campaigns."))
