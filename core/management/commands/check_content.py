from django.core.management.base import BaseCommand

from core.content import load_events, load_notices


class Command(BaseCommand):
    help = "Validate the JSON files used by the public site."

    def handle(self, *args, **options):
        events = load_events()
        notices = load_notices()
        self.stdout.write(
            self.style.SUCCESS(
                f"Content is valid: {len(events)} event(s), {len(notices)} notice(s)."
            )
        )
