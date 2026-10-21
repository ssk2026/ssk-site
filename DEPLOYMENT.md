# Production deployment notes

This project is a read-only Django site backed by JSON files. It does not use a
database, web admin, login, or public data-submission forms.

## Content updates

Use Pages CMS as described in `CONTENT_MANAGEMENT.md`, or edit the individual
JSON files under `content/events/`, `content/briefings/`, `content/papers/`, and
`content/notices/`. Then validate the files:

```powershell
.\venv\Scripts\python.exe manage.py check_content
```

The next page request reads the updated JSON. No application restart is needed.
Images and downloadable files belong under `media/`; use `/media/...` URLs in
the JSON records.

## Production environment

Configure these environment variables in the Windows service that runs Django:

```text
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=<long random production secret>
DJANGO_ALLOWED_HOSTS=ssk.dongguk.edu,210.94.162.155
DJANGO_HTTPS=true
```

Keep `DJANGO_HTTPS=false` until the domain, reverse proxy, and certificate are
working together. Turning it on enables HTTPS redirects and HSTS.

Before starting the application, collect static assets:

```powershell
.\venv\Scripts\python.exe manage.py collectstatic --noinput
```

Run the WSGI application with a production server such as Waitress, bound to
localhost behind IIS, Caddy, or another TLS-terminating reverse proxy. Configure
the reverse proxy to:

- listen on ports 80 and 443;
- redirect HTTP to HTTPS;
- provide the certificate for `ssk.dongguk.edu`;
- proxy application requests to the local WSGI server;
- serve `/media/` from the project's `media` directory;
- send `X-Forwarded-Proto: https` to Django.
