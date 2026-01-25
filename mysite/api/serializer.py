from rest_framework import serializers
from .models import Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["slug", "type", "title", "hero_image_url", "body",
                  "status", "published_at", "created_at", "updated_at"]
