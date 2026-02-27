from django.db import models

class Briefing(models.Model):
    title = models.CharField("제목", max_length=200)
    author = models.CharField("작성자", max_length=50)
    content = models.TextField("내용")
    image = models.ImageField("대표이미지", upload_to="briefing/", blank=True, null=True)
    created_at = models.DateField("작성일")
    views = models.PositiveIntegerField("조회수", default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    event_date = models.DateField(null=True, blank=True)  # 🔥 추가
    author = models.CharField(max_length=50, default="관리자")
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class EventImage(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='events/images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event.title} - 이미지"


# 📎 파일 전용
class EventAttachment(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='events/files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.title} - 첨부파일"


# 👁 조회수 중복 방지
class EventView(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)