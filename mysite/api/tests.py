from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from .models import Entry


User = get_user_model()


class EntriesCardsEndpointTests(TestCase):
    """Tests for the /entries/cards/ endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_entries_cards_requires_authentication(self):
        """Test that entries_cards endpoint requires authentication"""
        response = self.client.get('/entries/cards/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entries_cards_returns_only_published_cards(self):
        """Test that entries_cards returns only published card entries"""
        self.client.force_authenticate(user=self.user)

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

        response = self.client.get('/entries/cards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should only return published cards
        entry_ids = [entry['id'] if isinstance(
            entry, dict) else entry.id for entry in response.data]
        self.assertIn(published_card.id, entry_ids)
        self.assertNotIn(draft_card.id, entry_ids)
        self.assertNotIn(published_post.id, entry_ids)

    def test_entries_cards_returns_empty_list_when_no_published_cards(self):
        """Test that entries_cards returns empty list when no published cards exist"""
        self.client.force_authenticate(user=self.user)

        # Create only draft cards
        Entry.objects.create(
            title='Draft Card',
            body='Card body',
            type=Entry.Type.CARD,
            status=Entry.Status.DRAFT
        )

        response = self.client.get('/entries/cards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class EntriesPostsEndpointTests(TestCase):
    """Tests for the /entries/posts/ endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_entries_posts_requires_authentication(self):
        """Test that entries_posts endpoint requires authentication"""
        response = self.client.get('/entries/posts/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entries_posts_returns_only_published_posts(self):
        """Test that entries_posts returns only published post entries"""
        self.client.force_authenticate(user=self.user)

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

        response = self.client.get('/entries/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should only return published posts
        entry_ids = [entry['id'] if isinstance(
            entry, dict) else entry.id for entry in response.data]
        self.assertIn(published_post.id, entry_ids)
        self.assertNotIn(draft_post.id, entry_ids)
        self.assertNotIn(published_card.id, entry_ids)

    def test_entries_posts_returns_empty_list_when_no_published_posts(self):
        """Test that entries_posts returns empty list when no published posts exist"""
        self.client.force_authenticate(user=self.user)

        # Create only draft posts
        Entry.objects.create(
            title='Draft Post',
            body='Post body',
            type=Entry.Type.POST,
            status=Entry.Status.DRAFT
        )

        response = self.client.get('/entries/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


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

    def test_entries_all_requires_authentication(self):
        """Test that entries_all endpoint requires authentication"""
        response = self.client.get('/entries/all/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entries_all_requires_admin_permission(self):
        """Test that entries_all endpoint requires admin permission"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/entries/all/')
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

        response = self.client.get('/entries/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should return all entries
        entry_ids = [entry['id'] for entry in response.data]
        self.assertIn(published_card.id, entry_ids)
        self.assertIn(published_post.id, entry_ids)

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

        response = self.client.get('/entries/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        entry_data = response.data[0]
        # Check that all serializer fields are present
        self.assertIn('id', entry_data)
        self.assertIn('slug', entry_data)
        self.assertIn('title', entry_data)
        self.assertIn('hero_image_url', entry_data)
        self.assertIn('status', entry_data)
        self.assertIn('published_at', entry_data)
        self.assertIn('created_at', entry_data)
        self.assertIn('updated_at', entry_data)

        # Check that values match
        self.assertEqual(entry_data['id'], entry.id)
        self.assertEqual(entry_data['title'], entry.title)
        self.assertEqual(entry_data['slug'], entry.slug)
        self.assertEqual(entry_data['status'], entry.status)
        self.assertEqual(entry_data['hero_image_url'], entry.hero_image_url)

    def test_entries_all_returns_empty_list_when_no_entries(self):
        """Test that entries_all returns empty list when no entries exist"""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/entries/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class EntryModelTests(TestCase):
    """Tests for the Entry model"""

    def test_entry_creation(self):
        """Test creating an entry"""
        entry = Entry.objects.create(
            title='Test Entry',
            body='Test body',
            type=Entry.Type.POST,
            status=Entry.Status.DRAFT
        )
        self.assertEqual(entry.title, 'Test Entry')
        self.assertEqual(entry.body, 'Test body')
        self.assertEqual(entry.type, Entry.Type.POST)
        self.assertEqual(entry.status, Entry.Status.DRAFT)
        self.assertIsNotNone(entry.slug)
        self.assertIsNotNone(entry.created_at)
        self.assertIsNotNone(entry.updated_at)

    def test_entry_slug_generation(self):
        """Test that slug is automatically generated from title"""
        entry = Entry.objects.create(
            title='Test Entry Title',
            body='Test body',
            type=Entry.Type.POST
        )
        self.assertStartsWith(entry.slug, 'test-entry-title')

    def test_entry_defaults(self):
        """Test entry default values"""
        entry = Entry.objects.create(
            title='Test Entry',
            body='Test body'
        )
        self.assertEqual(entry.type, Entry.Type.POST)
        self.assertEqual(entry.status, Entry.Status.DRAFT)
        self.assertIsNone(entry.published_at)

    def test_entry_str_representation(self):
        """Test entry string representation"""
        entry = Entry.objects.create(
            title='Test Entry',
            body='Test body'
        )
        self.assertEqual(str(entry), 'Test Entry')
