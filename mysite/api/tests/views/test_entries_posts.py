from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Entry


class EntriesPostsViewTests(TestCase):
    """Tests for the entries_posts view"""

    def setUp(self):
        self.client = APIClient()

    def test_entries_posts_returns_only_published_posts(self):
        """Test that entries_posts returns only published post entries"""
        # Create test entries
        published_post = Entry.objects.create(
            title='Published Post',
            body='Post body',
            type=Entry.Type.POST,
            status=Entry.Status.PUBLISHED,
            published_at=timezone.now()
        )
        draft_post = Entry.objects.create(
            title='Draft Post',
            body='Post body',
            type=Entry.Type.POST,
            status=Entry.Status.DRAFT
        )
        published_card = Entry.objects.create(
            title='Published Card',
            body='Card body',
            type=Entry.Type.CARD,
            status=Entry.Status.PUBLISHED,
            published_at=timezone.now()
        )

        response = self.client.get('/entries/posts/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should only return published posts
        entry_slugs = [entry['slug'] for entry in response.data]
        self.assertIn(published_post.slug, entry_slugs)
        self.assertNotIn(draft_post.slug, entry_slugs)
        self.assertNotIn(published_card.slug, entry_slugs)

    def test_entries_posts_returns_empty_list_when_no_published_posts(self):
        """Test that entries_posts returns empty list when no published posts exist"""
        # Create only draft posts
        Entry.objects.create(
            title='Draft Post',
            body='Post body',
            type=Entry.Type.POST,
            status=Entry.Status.DRAFT
        )

        response = self.client.get('/entries/posts/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
