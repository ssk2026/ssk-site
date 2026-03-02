from django.db import models


class Event(models.Model):

    TYPE_CHOICES = (
        ('event', '주요행사'),
        ('briefing', '성과브리핑'),
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='event'
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    event_date = models.DateField(null=True, blank=True)
    author = models.CharField(max_length=50, default="관리자")
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

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


class EventView(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)


class Notice(models.Model):
    title = models.CharField("제목", max_length=200)
    content = models.TextField("내용")
    author = models.CharField("작성자", max_length=50, default="관리자")
    created_at = models.DateField("작성일")
    views = models.PositiveIntegerField("조회수", default=0)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class Inquiry(models.Model):
    name = models.CharField("이름", max_length=100)
    email = models.EmailField("이메일")
    subject = models.CharField("문의 제목", max_length=200)
    message = models.TextField("문의 내용")
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return f"[{self.created_at:%Y-%m-%d}] {self.name} - {self.subject}"