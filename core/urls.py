from django.urls import path, include
from django.views.generic.base import RedirectView
from . import views


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/images/remove_background.png', permanent=True)),

    # Home
    path('', views.home, name='home'),

    # About
    path('about/overview/', views.overview, name='overview'),
    path('about/people/', views.people, name='people'),
    path('about/intro/', views.about_intro, name='about_intro'),

    # Performance
    path('performance/papers/', views.performance_papers, name='performance_papers'),
    path('performance/briefing/', views.performance_briefing, name='performance_briefing'),
    path('performance/business-plan/', views.performance_business_plan, name='performance_business_plan'),

    # Events
    path('events/', views.event_list, name='events'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),

    # Briefing detail
    path('performance/briefing/<int:id>/', views.event_detail, name='briefing_detail'),

    # Notice / Contact
    path('notice/', views.notice_list, name='notice_list'),
    path('notice/<int:id>/', views.notice_detail, name='notice_detail'),
    path('contact/', views.contact, name='contact'),

    # Admin CRUD
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:id>/update/', views.event_update, name='event_update'),
    path('events/<int:id>/delete/', views.event_delete, name='event_delete'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
