from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Entry
from .serializer import EntrySerializer


@api_view(["GET"])
def health(request):
    return Response({"ok": True})


@api_view(["GET"])
def entries_cards(request):
    entries = Entry.objects.filter(
        status=Entry.Status.PUBLISHED, type=Entry.Type.CARD)
    serialized_cards = EntrySerializer(entries, many=True)

    return Response(serialized_cards.data)


@api_view(["GET"])
def entries_posts(request):
    entries = Entry.objects.filter(
        status=Entry.Status.PUBLISHED, type=Entry.Type.POST)
    serialized_posts = EntrySerializer(entries, many=True)

    return Response(serialized_posts.data)


@api_view(["GET"])
def entries_post_slug(request, slug):
    try:
        entry = Entry.objects.get(
            type=Entry.Type.POST, status=Entry.Status.PUBLISHED, slug=slug)
    except Entry.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    serialized_entry = EntrySerializer(entry)
    return Response(serialized_entry.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def entries_all(request):
    entries = Entry.objects.all()
    serialized_entries = EntrySerializer(entries, many=True)

    return Response(serialized_entries.data)
