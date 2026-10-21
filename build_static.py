import os
import shutil
from pathlib import Path


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django


django.setup()

from django.conf import settings
from django.core.management import call_command
from django.test import Client, override_settings
from django.urls import reverse

from core.content import load_events, load_notices


BASE_DIR = Path(settings.BASE_DIR).resolve()
OUTPUT_DIR = BASE_DIR / "dist"


def output_file(url):
    if url == "/":
        return OUTPUT_DIR / "index.html"
    return OUTPUT_DIR / url.strip("/") / "index.html"


def render_page(client, url, *, static_list=False):
    query = {"_static": "1"} if static_list else None
    response = client.get(url, query, HTTP_HOST="localhost")
    if response.status_code != 200:
        raise RuntimeError(f"Could not export {url}: HTTP {response.status_code}")

    destination = output_file(url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)
    print(f"rendered {url} -> {destination.relative_to(BASE_DIR)}")


def build():
    if OUTPUT_DIR.parent != BASE_DIR:
        raise RuntimeError("Static output must stay inside the project directory")

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    call_command("check")
    call_command("check_content")

    with override_settings(STATIC_ROOT=OUTPUT_DIR / "static"):
        call_command("collectstatic", interactive=False, verbosity=0)

    if settings.MEDIA_ROOT.exists():
        shutil.copytree(settings.MEDIA_ROOT, OUTPUT_DIR / "media")

    client = Client()
    pages = [
        (reverse("home"), False),
        (reverse("overview"), False),
        (reverse("about_intro"), False),
        (reverse("people"), False),
        (reverse("participants_organization"), False),
        (reverse("participants_professors"), False),
        (reverse("participants_postdocs"), False),
        (reverse("participants_assistants"), False),
        (reverse("performance_papers"), False),
        (reverse("performance_business_plan"), False),
        (reverse("performance_briefing"), True),
        (reverse("events"), True),
        (reverse("notice_list"), True),
        (reverse("contact"), False),
    ]

    for event in load_events():
        route_name = "briefing_detail" if event["type"] == "briefing" else "event_detail"
        pages.append((reverse(route_name, args=[event["id"]]), False))
    for notice in load_notices():
        pages.append((reverse("notice_detail", args=[notice["id"]]), False))

    for url, static_list in pages:
        render_page(client, url, static_list=static_list)

    favicon_source = OUTPUT_DIR / "static" / "images" / "remove_background.png"
    if favicon_source.exists():
        shutil.copy2(favicon_source, OUTPUT_DIR / "favicon.ico")

    (OUTPUT_DIR / "_headers").write_text(
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n"
        "\n"
        "/static/*\n"
        "  Cache-Control: public, max-age=31536000, immutable\n"
        "\n"
        "/media/*\n"
        "  Cache-Control: public, max-age=86400\n",
        encoding="utf-8",
    )

    print(f"Static site ready: {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
