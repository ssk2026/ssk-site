from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 소개
    path('about/overview/', views.overview, name='overview'),
    path('about/people/', views.senior_researchers, name='people'),
    path('about/people/fulltime/', views.fulltime_researchers, name='fulltime'),
    path('about/people/assistants/', views.assistants, name='assistants'),

    # 연구성과
    path('performance/papers/', views.performance_papers, name='performance_papers'),
    path('performance/briefing/', views.performance_briefing, name='performance_briefing'),

    path('events/', views.event_list, name='events'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),
    path('contact/', views.contact, name='contact'),
    path('performance/briefing/', views.performance_briefing, name='performance_briefing'),
    path('performance/briefing/<int:pk>/', views.briefing_detail, name='briefing_detail'),

]
