import json
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


CONTENT_DIR = Path(settings.BASE_DIR) / "content"


def _load_collection(filename, required_fields):
    path = CONTENT_DIR / filename

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ImproperlyConfigured(f"Missing content file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ImproperlyConfigured(
            f"Invalid JSON in {path.name} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc

    if not isinstance(payload, list):
        raise ImproperlyConfigured(f"{path.name} must contain a JSON array")

    seen_ids = set()
    for index, record in enumerate(payload, start=1):
        if not isinstance(record, dict):
            raise ImproperlyConfigured(f"{path.name} item {index} must be an object")

        missing = required_fields.difference(record)
        if missing:
            fields = ", ".join(sorted(missing))
            raise ImproperlyConfigured(f"{path.name} item {index} is missing: {fields}")

        if not isinstance(record["id"], int):
            raise ImproperlyConfigured(f"{path.name} item {index} has a non-integer id")
        if record["id"] in seen_ids:
            raise ImproperlyConfigured(f"{path.name} contains duplicate id {record['id']}")
        seen_ids.add(record["id"])

    return payload


def load_events(event_type=None):
    events = _load_collection(
        "events.json",
        {
            "id",
            "type",
            "title",
            "author",
            "event_date",
            "created_at",
            "main_image",
            "content_html",
            "attachments",
        },
    )

    for event in events:
        if event["type"] not in {"event", "briefing"}:
            raise ImproperlyConfigured(
                f"events.json item {event['id']} has invalid type {event['type']!r}"
            )
        if not isinstance(event["attachments"], list):
            raise ImproperlyConfigured(
                f"events.json item {event['id']} attachments must be an array"
            )

    if event_type:
        events = [event for event in events if event["type"] == event_type]

    if event_type == "briefing":
        return sorted(events, key=lambda event: event["event_date"], reverse=True)

    return sorted(events, key=lambda event: event["created_at"], reverse=True)


def load_notices():
    notices = _load_collection(
        "notices.json",
        {"id", "title", "author", "created_at", "content_html"},
    )
    return sorted(notices, key=lambda notice: notice["created_at"], reverse=True)


def find_by_id(records, record_id):
    return next((record for record in records if record["id"] == record_id), None)
