from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.other_user = User.objects.create(username='Михаил Булгаков')
        cls.author_note = Note.objects.create(
            title='Заметка Толстого',
            text='Текст заметки Толстого',
            slug='tolstoy_slug',
            author=cls.author
        )
        cls.other_note = Note.objects.create(
            title='Заметка Булгакова',
            text='Текст заметки Булгакова',
            slug='bulgakov_slug',
            author=cls.other_user
        )

    def test_own_note_in_list(self):
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.author_note, response.context['object_list'])

    def test_no_other_user_notes_in_list(self):
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.other_note, response.context['object_list'])

    def test_forms_on_add_and_edit_pages(self):
        self.client.force_login(self.author)
        urls = (
            reverse('notes:add'),
            reverse('notes:edit', args=(self.author_note.slug,))
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
