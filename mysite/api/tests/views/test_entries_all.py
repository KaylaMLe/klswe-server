from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from api.models import Entry


User = get_user_model()


class EntriesAllEndpointTests(TestCase):
    """Tests for the /entries/all/ endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )

    def test_entries_all_requires_admin_permission(self):
        """Test that entries_all endpoint requires admin permission"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/entries/all/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_entries_all_returns_all_entries_when_admin(self):
        """Test that entries_all returns all entries when accessed by admin"""
        self.client.force_authenticate(user=self.admin_user)

        # Create test entries with different statuses and types
        published_card = Entry.objects.create(
            title='Published Card',
            body='Card body',
            type=Entry.Type.CARD,
            status=Entry.Status.PUBLISHED,
            published_at=timezone.now()
        )
        published_post = Entry.objects.create(
            title='Published Post',
            body='Post body',
            type=Entry.Type.POST,
            status=Entry.Status.PUBLISHED,
            published_at=timezone.now()
        )

        response = self.client.get('/entries/all/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should return all entries
        entry_slugs = [entry['slug'] for entry in response.data]
        self.assertIn(published_card.slug, entry_slugs)
        self.assertIn(published_post.slug, entry_slugs)

    def test_entries_all_returns_serialized_data(self):
        """Test that entries_all returns properly serialized data"""
        self.client.force_authenticate(user=self.admin_user)

        entry = Entry.objects.create(
            title='Test Entry',
            body='Test body',
            type=Entry.Type.POST,
            status=Entry.Status.PUBLISHED,
            published_at=timezone.now(),
            hero_image_url='https://example.com/image.jpg'
        )

        response = self.client.get('/entries/all/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        entry_data = response.data[0]
        # Check that all serializer fields are present
        self.assertIn('slug', entry_data)
        self.assertIn('title', entry_data)
        self.assertIn('hero_image_url', entry_data)
        self.assertIn('status', entry_data)
        self.assertIn('published_at', entry_data)
        self.assertIn('created_at', entry_data)
        self.assertIn('updated_at', entry_data)

        # Check that values match
        self.assertEqual(entry_data['slug'], entry.slug)
        self.assertEqual(entry_data['title'], entry.title)
        self.assertEqual(entry_data['status'], entry.status)
        self.assertEqual(entry_data['hero_image_url'], entry.hero_image_url)

    def test_entries_all_returns_empty_list_when_no_entries(self):
        """Test that entries_all returns empty list when no entries exist"""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/entries/all/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
