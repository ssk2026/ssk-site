from django.core.management.base import BaseCommand

from core.content import load_events, load_notices, load_papers


class Command(BaseCommand):
    help = "Validate the JSON files used by the public site."

    def handle(self, *args, **options):
        events = load_events()
        notices = load_notices()
        papers = load_papers()
        self.stdout.write(
            self.style.SUCCESS(
                "Content is valid: "
                f"{len(events)} event(s), {len(papers)} paper(s), "
                f"{len(notices)} notice(s)."
            )
        )
