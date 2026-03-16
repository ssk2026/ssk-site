from django.contrib import admin
from .models import Event, EventImage, EventAttachment, Inquiry


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

    # 🔥 추가된 부분
    list_display = ("title", "type", "event_date", "views")
    list_filter = ("type", "event_date")
    search_fields = ("title", "content")
    ordering = ("-created_at",)


admin.site.register(Event, EventAdmin)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

class EventImageInline(admin.StackedInline):
    model = EventImage
    extra = 1
    max_num = 1