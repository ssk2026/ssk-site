# JSON content guide

The public site reads content directly from the JSON files in this directory.
There is no web admin page, login, or browser-based upload feature.

## Editing content

1. Make a backup copy of the JSON file you are changing.
2. Add or edit an object in `events.json` or `notices.json`.
3. Keep every `id` unique and use double quotes around JSON strings.
4. Put images and attachments under `media/` and use a `/media/...` path.
5. Run `python manage.py check_content` before publishing the change.

Changes are read on the next request, so the web process does not need to be
restarted after a valid JSON edit.

## Event fields

- `id`: unique integer
- `type`: `event` or `briefing`
- `title`: title shown in lists and detail pages
- `author`: display name, normally `관리자`
- `event_date`: event date in `YYYY-MM-DD` form, or an empty string
- `created_at`: publication date in `YYYY-MM-DD` form
- `main_image`: thumbnail path, or an empty string
- `content_html`: trusted HTML for the detail page
- `attachments`: list of objects with `name` and `url`

## Notice fields

- `id`: unique integer
- `title`: notice title
- `author`: display name
- `created_at`: publication date in `YYYY-MM-DD` form
- `content_html`: trusted HTML for the detail page
