from django.urls import path
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

    # Participants
    path('participants/organization/', views.participants_organization, name='participants_organization'),
    path('participants/professors/', views.participants_professors, name='participants_professors'),
    path('participants/postdocs/', views.participants_postdocs, name='participants_postdocs'),
    path('participants/assistants/', views.participants_assistants, name='participants_assistants'),

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

]
