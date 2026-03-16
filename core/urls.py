from django.urls import path, include
from . import views


urlpatterns = [

    # 홈
    path('', views.home, name='home'),

    # 소개
    path('about/overview/', views.overview, name='overview'),
    path('about/people/', views.people, name='people'),
    path('about/intro/', views.about_intro, name='about_intro'),
    path('about/organization/', views.about_organization, name='about_organization'),


    # 연구성과
    path('performance/papers/', views.performance_papers, name='performance_papers'),
    path('performance/briefing/', views.performance_briefing, name='performance_briefing'),

    # 주요행사
    path('events/', views.event_list, name='events'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),

    # 성과브리핑 상세 (event_detail 재사용)
    path('performance/briefing/<int:id>/', views.event_detail, name='briefing_detail'),

    # 공지사항
    path('notice/', views.notice_list, name='notice_list'),

    # 문의
    path('contact/', views.contact, name='contact'),

    # 관리자 CRUD
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:id>/update/', views.event_update, name='event_update'),
    path('events/<int:id>/delete/', views.event_delete, name='event_delete'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]