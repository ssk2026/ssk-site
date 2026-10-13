from pathlib import Path
from urllib.parse import quote

from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.utils.html import strip_tags

from .content import find_by_id, load_events, load_notices


def home(request):
    return render(request, "home.html")


def overview(request):
    return render(request, "about_overview.html")


def about_intro(request):
    return render(request, "about_intro.html")


def people(request):
    return render(request, "people.html")


def participants_organization(request):
    return render(request, "participants_organization.html")


def participants_professors(request):
    return render(request, "participants_professors.html")


def participants_postdocs(request):
    return render(request, "participants_postdocs.html")


def participants_assistants(request):
    return render(request, "participants_assistants.html")


def performance_papers(request):
    return render(request, "core/performance_papers.html")


def performance_business_plan(request):
    proposals_dir = Path(settings.MEDIA_ROOT) / "proposals"
    proposal_file_url = ""

    if proposals_dir.exists():
        proposal_files = sorted(
            (
                file
                for file in proposals_dir.iterdir()
                if file.is_file() and file.suffix.lower() == ".pdf"
            ),
            key=lambda file: file.name,
        )
        if proposal_files:
            proposal_file_url = (
                f"{settings.MEDIA_URL}proposals/{quote(proposal_files[0].name)}"
            )

    try:
        initial_page = max(1, int(request.GET.get("page", 1)))
    except (TypeError, ValueError):
        initial_page = 1

    return render(
        request,
        "core/performance_business_plan.html",
        {"proposal_file_url": proposal_file_url, "initial_page": initial_page},
    )


def contact(request):
    return render(request, "contact.html")


def _filtered_events(request, event_type):
    events = load_events(event_type)
    query = request.GET.get("q", "").strip()
    search_type = request.GET.get("type", "title")

    if query:
        lowered_query = query.casefold()
        if search_type == "content":
            events = [
                event
                for event in events
                if lowered_query in strip_tags(event["content_html"]).casefold()
            ]
        else:
            events = [
                event
                for event in events
                if lowered_query in event["title"].casefold()
            ]

    return events, query, search_type


def event_list(request):
    events, query, search_type = _filtered_events(request, "event")
    page_obj = Paginator(events, 5).get_page(request.GET.get("page"))
    return render(
        request,
        "events.html",
        {
            "page_obj": page_obj,
            "total_count": len(events),
            "q": query,
            "type": search_type,
        },
    )


def performance_briefing(request):
    briefings, query, search_type = _filtered_events(request, "briefing")
    page_obj = Paginator(briefings, 5).get_page(request.GET.get("page"))
    return render(
        request,
        "core/performance_briefing.html",
        {
            "page_obj": page_obj,
            "total_count": len(briefings),
            "q": query,
            "type": search_type,
        },
    )


def event_detail(request, id):
    event = find_by_id(load_events(), id)
    if event is None:
        raise Http404("해당 게시물을 찾을 수 없습니다.")
    return render(request, "event_detail.html", {"event": event})


def notice_list(request):
    notices = load_notices()
    query = request.GET.get("q", "").strip()
    if query:
        lowered_query = query.casefold()
        notices = [
            notice
            for notice in notices
            if lowered_query in notice["title"].casefold()
        ]

    page_obj = Paginator(notices, 10).get_page(request.GET.get("page"))
    return render(
        request,
        "notice_list.html",
        {"page_obj": page_obj, "total_count": len(notices), "q": query},
    )


def notice_detail(request, id):
    notice = find_by_id(load_notices(), id)
    if notice is None:
        raise Http404("해당 공지사항을 찾을 수 없습니다.")
    return render(request, "notice_detail.html", {"notice": notice})
