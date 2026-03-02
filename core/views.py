from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required

from .models import Event, EventImage, EventView, Notice, Inquiry
from .forms import EventForm


# =========================
# 홈
# =========================

def home(request):
    main_images = EventImage.objects.filter(is_main=True)

    latest_events = Event.objects.prefetch_related(
        Prefetch('images', queryset=main_images, to_attr='main_image')
    ).order_by('-created_at')[:2]

    return render(request, 'home.html', {
        'latest_events': latest_events
    })


# =========================
# 정적 페이지
# =========================

def about(request): return render(request, 'about.html')
def overview(request): return render(request, 'about_overview.html')
def people(request): return render(request, 'people.html')
def senior_researchers(request): return render(request, 'senior.html')
def fulltime_researchers(request): return render(request, 'fulltime.html')
def assistants(request): return render(request, 'assistants.html')
def others(request): return render(request, 'others.html')
def outputs(request): return render(request, 'outputs.html')
def performance_overview(request): return render(request, 'core/performance_overview.html')
def performance_papers(request): return render(request, 'core/performance_papers.html')


# =========================
# 문의하기
# =========================

def contact(request):
    if request.method == "POST":
        Inquiry.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )
        return redirect("contact")

    return render(request, 'contact.html')


# =========================
# 주요행사 (type='event')
# =========================

def event_list(request):
    event_list = Event.objects.filter(type='event').order_by('-created_at')

    q = request.GET.get('q')
    search_type = request.GET.get('type')

    if q:
        if search_type == 'title':
            event_list = event_list.filter(title__icontains=q)
        elif search_type == 'content':
            event_list = event_list.filter(content__icontains=q)
        else:
            event_list = event_list.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            )

    paginator = Paginator(event_list, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'events.html', {
        'page_obj': page_obj,
        'total_count': event_list.count(),
        'q': q,
        'type': search_type,
    })


# =========================
# 성과브리핑 (type='briefing')
# =========================

def performance_briefing(request):
    briefing_list = Event.objects.filter(type='briefing').order_by('-created_at')

    q = request.GET.get('q')
    search_type = request.GET.get('type')

    if q:
        if search_type == 'content':
            briefing_list = briefing_list.filter(content__icontains=q)
        else:
            briefing_list = briefing_list.filter(title__icontains=q)

    paginator = Paginator(briefing_list, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'core/performance_briefing.html', {
        'page_obj': page_obj,
        'total_count': briefing_list.count(),
        'q': q,
        'type': search_type,
    })


# =========================
# 상세페이지 (공통)
# =========================

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


def event_detail(request, id):
    event = get_object_or_404(Event, id=id)

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


# =========================
# 공지사항
# =========================

def notice_list(request):
    notice_list = Notice.objects.all()

    q = request.GET.get('q')
    if q:
        notice_list = notice_list.filter(title__icontains=q)

    paginator = Paginator(notice_list, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'notice_list.html', {
        'page_obj': page_obj,
        'total_count': notice_list.count(),
        'q': q,
    })


# =========================
# 관리자 전용 CRUD
# =========================

@staff_member_required
def event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'event_form.html', {'form': form})


@staff_member_required
def event_update(request, id):
    event = get_object_or_404(Event, id=id)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_detail', id=event.id)
    return render(request, 'event_form.html', {'form': form})


@staff_member_required
def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})