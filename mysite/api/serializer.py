from rest_framework import serializers
from .models import Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["id", "slug", "title", "hero_image_url",
                  "status", "published_at", "created_at", "updated_at"]
