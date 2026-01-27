from django.test import TestCase

from api.models import Entry


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
        self.assertEqual(entry.slug, 'test-entry-title')

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
