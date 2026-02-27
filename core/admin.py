from django.contrib import admin
from .models import Event, EventImage, EventAttachment


# 🖼 이미지 Inline
class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1
    fields = ('image', 'is_main')
    verbose_name = "행사 이미지"
    verbose_name_plural = "행사 이미지들"


# 📎 파일 Inline
class EventAttachmentInline(admin.TabularInline):
    model = EventAttachment
    extra = 1
    fields = ('file',)
    verbose_name = "첨부파일"
    verbose_name_plural = "첨부파일들"


class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageInline, EventAttachmentInline]


admin.site.register(Event, EventAdmin)