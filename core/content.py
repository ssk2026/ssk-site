import json
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


CONTENT_DIR = Path(settings.BASE_DIR) / "content"


def _load_collection(directory_name, required_fields):
    directory = CONTENT_DIR / directory_name
    if not directory.is_dir():
        raise ImproperlyConfigured(f"Missing content directory: {directory}")

    records = []
    seen_slugs = set()
    seen_ids = set()
    for path in sorted(directory.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ImproperlyConfigured(
                f"Invalid JSON in {path.name} at line {exc.lineno}, "
                f"column {exc.colno}: {exc.msg}"
            ) from exc

        if not isinstance(record, dict):
            raise ImproperlyConfigured(f"{path.name} must contain a JSON object")

        missing = required_fields.difference(record)
        if missing:
            fields = ", ".join(sorted(missing))
            raise ImproperlyConfigured(f"{path.name} is missing: {fields}")

        slug = path.stem
        if slug in seen_slugs:
            raise ImproperlyConfigured(f"Duplicate content slug: {slug}")
        seen_slugs.add(slug)

        if "id" in record:
            if not isinstance(record["id"], int):
                raise ImproperlyConfigured(f"{path.name} has a non-integer id")
            if record["id"] in seen_ids:
                raise ImproperlyConfigured(f"Duplicate content id: {record['id']}")
            seen_ids.add(record["id"])

        record["slug"] = slug
        records.append(record)

    return records


def load_events(event_type=None):
    required_fields = {
        "type",
        "title",
        "created_at",
    }
    events = _load_collection("events", required_fields)
    events.extend(_load_collection("briefings", required_fields))

    for event in events:
        event.setdefault("author", "관리자")
        event.setdefault("event_date", "")
        event.setdefault("main_image", "")
        event.setdefault("summary", "")
        event.setdefault("content_html", "")
        event.setdefault("attachments", [])
        event.setdefault("published", True)
        if event["type"] not in {"event", "briefing"}:
            raise ImproperlyConfigured(
                f"{event['slug']}.json has invalid type {event['type']!r}"
            )
        if not isinstance(event["attachments"], list):
            raise ImproperlyConfigured(
                f"{event['slug']}.json attachments must be an array"
            )

    events = [event for event in events if event.get("published", True)]

    if event_type:
        events = [event for event in events if event["type"] == event_type]

    if event_type == "briefing":
        return sorted(events, key=lambda event: event["event_date"], reverse=True)

    return sorted(events, key=lambda event: event["created_at"], reverse=True)


def load_notices():
    notices = _load_collection(
        "notices",
        {"title", "created_at"},
    )
    for notice in notices:
        notice.setdefault("author", "관리자")
        notice.setdefault("content_html", "")
        notice.setdefault("published", True)
    notices = [notice for notice in notices if notice.get("published", True)]
    return sorted(notices, key=lambda notice: notice["created_at"], reverse=True)


def load_papers():
    papers = _load_collection(
        "papers",
        {"title", "year", "citation_html"},
    )
    for paper in papers:
        paper.setdefault("published", True)
    papers = [paper for paper in papers if paper.get("published", True)]
    return sorted(
        papers,
        key=lambda paper: (paper["year"], paper["title"]),
        reverse=True,
    )


def find_by_slug(records, record_slug):
    return next(
        (record for record in records if record["slug"] == str(record_slug)),
        None,
    )
