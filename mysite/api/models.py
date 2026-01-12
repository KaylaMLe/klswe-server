from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField


class Entry(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    class Type(models.TextChoices):
        POST = "post", "Post"
        CARD = "card", "Card"

    slug = AutoSlugField(populate_from='title',
                         unique=True, always_update=False)
    type = models.CharField(
        max_length=12,
        choices=Type.choices,
        default=Type.POST,
    )

    title = models.CharField(max_length=200)
    hero_image_url = models.URLField(blank=True)

    body = models.TextField()

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    published_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self) -> str:
        return self.title
