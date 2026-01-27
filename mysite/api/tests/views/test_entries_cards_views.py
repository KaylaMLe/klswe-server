from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Entry


class EntriesCardsViewTests(TestCase):
    """Tests for the entries_cards view"""

    def setUp(self):
        self.client = APIClient()

    def test_entries_cards_returns_only_published_cards(self):
        """Test that entries_cards returns only published card entries"""
        # Create test entries
        published_card = Entry.objects.create(
            title='Published Card',
            body='Card body',
            type=Entry.Type.CARD,
            status=Entry.Status.PUBLISHED,
            published_at=timezone.now()
        )
        draft_card = Entry.objects.create(
            title='Draft Card',
            body='Card body',
            type=Entry.Type.CARD,
            status=Entry.Status.DRAFT
        )
        published_post = Entry.objects.create(
            title='Published Post',
            body='Post body',
            type=Entry.Type.POST,
            status=Entry.Status.PUBLISHED,
            published_at=timezone.now()
        )

        response = self.client.get('/entries/cards/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should only return published cards
        entry_slugs = [entry['slug'] for entry in response.data]
        self.assertIn(published_card.slug, entry_slugs)
        self.assertNotIn(draft_card.slug, entry_slugs)
        self.assertNotIn(published_post.slug, entry_slugs)

    def test_entries_cards_returns_empty_list_when_no_published_cards(self):
        """Test that entries_cards returns empty list when no published cards exist"""
        # Create only draft cards
        Entry.objects.create(
            title='Draft Card',
            body='Card body',
            type=Entry.Type.CARD,
            status=Entry.Status.DRAFT
        )

        response = self.client.get('/entries/cards/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
