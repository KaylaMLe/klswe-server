from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from api.models import Entry


class EntriesPostSlugViewTests(TestCase):
    """Tests for the entries_post_slug view"""

    def setUp(self):
        self.client = APIClient()

    def test_entries_post_slug_returns_published_post(self):
        """Test that entries_post_slug returns a published entry by slug"""
        published_entry = Entry.objects.create(
            title='Published Post',
            body='Post body',
            type=Entry.Type.POST,
            status=Entry.Status.PUBLISHED,
            published_at=timezone.now()
        )

        response = self.client.get(
            f'/entries/post/{published_entry.slug}/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], published_entry.slug)
        self.assertEqual(response.data['title'], published_entry.title)
        self.assertEqual(response.data['body'], published_entry.body)

    def test_entries_post_slug_returns_404_for_draft_entry(self):
        """Test that entries_post_slug returns 404 for draft entries"""
        draft_entry = Entry.objects.create(
            title='Draft Post',
            body='Post body',
            type=Entry.Type.POST,
            status=Entry.Status.DRAFT
        )

        response = self.client.get(
            f'/entries/post/{draft_entry.slug}/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Post not found')

    def test_entries_post_slug_returns_404_for_nonexistent_slug(self):
        """Test that entries_post_slug returns 404 for non-existent slugs"""
        response = self.client.get(
            '/entries/post/nonexistent-slug/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_entries_post_slug_returns_serialized_data(self):
        """Test that entries_post_slug returns properly serialized data"""
        entry = Entry.objects.create(
            title='Test Entry',
            body='Test body content',
            type=Entry.Type.POST,
            status=Entry.Status.PUBLISHED,
            published_at=timezone.now(),
            hero_image_url='https://example.com/image.jpg'
        )

        response = self.client.get(f'/entries/post/{entry.slug}/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that all serializer fields are present
        self.assertIn('slug', response.data)
        self.assertIn('title', response.data)
        self.assertIn('body', response.data)
        self.assertIn('hero_image_url', response.data)
        self.assertIn('status', response.data)
        self.assertIn('published_at', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
        self.assertIn('type', response.data)

        # Check that values match
        self.assertEqual(response.data['slug'], entry.slug)
        self.assertEqual(response.data['title'], entry.title)
        self.assertEqual(response.data['body'], entry.body)
        self.assertEqual(response.data['status'], entry.status)
        self.assertEqual(response.data['hero_image_url'], entry.hero_image_url)
        self.assertEqual(response.data['type'], entry.type)

    def test_entries_post_slug_rejects_card_type(self):
        """Test that entries_post_slug returns 404 for Card type, even if published"""
        card_entry = Entry.objects.create(
            title='Published Card',
            body='Card body',
            type=Entry.Type.CARD,
            status=Entry.Status.PUBLISHED,
            published_at=timezone.now()
        )

        response = self.client.get(
            f'/entries/post/{card_entry.slug}/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
