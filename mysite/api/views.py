from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Entry


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def health(request):
    return Response({"ok": True})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def entries_cards(request):
    entries = Entry.objects.filter(
        status=Entry.Status.PUBLISHED, type=Entry.Type.CARD)
    return Response(entries)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def entries_posts(request):
    entries = Entry.objects.filter(
        status=Entry.Status.PUBLISHED, type=Entry.Type.POST)
    return Response(entries)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def entries_all(request):
    entries = Entry.objects.all()
    return Response(entries)
