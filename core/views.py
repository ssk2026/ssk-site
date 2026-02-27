from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from .models import Briefing, Event, EventView


# =========================
# 홈 / 기본 페이지
# =========================

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def overview(request):
    return render(request, 'about_overview.html')


def people(request):
    return render(request, 'people.html')


def senior_researchers(request):
    return render(request, 'senior.html')


def fulltime_researchers(request):
    return render(request, 'fulltime.html')


def assistants(request):
    return render(request, 'assistants.html')


def others(request):
    return render(request, 'others.html')


def outputs(request):
    return render(request, 'outputs.html')


def contact(request):
    return render(request, 'contact.html')


def performance_overview(request):
    return render(request, 'core/performance_overview.html')


def performance_papers(request):
    return render(request, 'core/performance_papers.html')


# =========================
# 연구성과 - 성과브리핑
# =========================

def performance_briefing(request):
    briefing_list = Briefing.objects.all().order_by('-created_at')

    # 🔎 검색
    q = request.GET.get('q')
    search_type = request.GET.get('type')

    if q:
        if search_type == 'content':
            briefing_list = briefing_list.filter(content__icontains=q)
        else:
            briefing_list = briefing_list.filter(title__icontains=q)

    paginator = Paginator(briefing_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_count': briefing_list.count(),
        'q': q,
        'type': search_type,
    }

    return render(request, 'core/performance_briefing.html', context)


def briefing_detail(request, pk):
    briefing = get_object_or_404(Briefing, pk=pk)

    # 단순 조회수 증가 (중복 방지는 필요 없다고 가정)
    briefing.views += 1
    briefing.save()

    return render(request, 'briefing_detail.html', {'briefing': briefing})


# =========================
# 주요행사
# =========================

def event_list(request):
    event_list = Event.objects.all().order_by('-created_at')

    # 🔎 검색
    q = request.GET.get('q')
    search_type = request.GET.get('type')

    if q:
        if search_type == 'title':
            event_list = event_list.filter(title__icontains=q)
        elif search_type == 'content':
            event_list = event_list.filter(content__icontains=q)
        else:
            event_list = event_list.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )

    paginator = Paginator(event_list, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'total_count': event_list.count(),
        'q': q,
        'type': search_type,
    }

    return render(request, 'events.html', context)


# 🔥 IP 추출 함수
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def event_detail(request, id):
    event = get_object_or_404(Event, id=id)

    # 🔥 조회수 중복 방지 (IP 기준 24시간)
    ip = get_client_ip(request)
    one_day_ago = timezone.now() - timedelta(days=1)

    already_viewed = EventView.objects.filter(
        event=event,
        ip_address=ip,
        viewed_at__gte=one_day_ago
    ).exists()

    if not already_viewed:
        event.views += 1
        event.save()
        EventView.objects.create(event=event, ip_address=ip)

    return render(request, 'event_detail.html', {'event': event})