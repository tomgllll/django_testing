from http import HTTPStatus

from pytils.translit import slugify

from .base_test_setup import (
    BaseTestSetup,
    NOTES_ADD_URL,
    NOTES_EDIT_URL_AUTHOR,
    NOTES_DELETE_URL_AUTHOR,
    NOTES_SUCCESS)
from notes.models import Note


class TestNoteCreation(BaseTestSetup):

    def test_logged_in_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertRedirects(response, NOTES_SUCCESS)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        initial_count = Note.objects.count()
        self.client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertEqual(Note.objects.count(), initial_count)

    def test_slug_generated_if_missing(self):
        Note.objects.all().delete()
        form_data = self.form_data.copy()
        form_data.pop('slug', None)
        self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(note.slug, expected_slug)


class TestNoteEditDelete(BaseTestSetup):

    def test_author_can_edit_note(self):
        response = self.author_client.post(NOTES_EDIT_URL_AUTHOR,
                                           data=self.form_data)
        self.assertRedirects(response, NOTES_SUCCESS)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.text, self.form_data['text'])
        self.assertEqual(updated_note.title, self.form_data['title'])
        self.assertEqual(updated_note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.other_user_client.post(NOTES_EDIT_URL_AUTHOR,
                                               data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.text, self.note.text)
        self.assertEqual(updated_note.title, self.note.title)
        self.assertEqual(updated_note.author, self.note.author)

    def test_author_can_delete_note(self):
        response = self.author_client.delete(NOTES_DELETE_URL_AUTHOR)
        self.assertRedirects(response, NOTES_SUCCESS)
        self.assertFalse(Note.objects.filter(slug='author_slug').exists())

    def test_user_cant_delete_note_of_another_user(self):
        response = self.other_user_client.delete(NOTES_DELETE_URL_AUTHOR)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(slug='author_slug').exists())
