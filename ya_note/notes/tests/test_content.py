from http import HTTPStatus

from .base_test_setup import (
    BaseTestSetup,
    NOTES_LIST_URL,
    NOTES_ADD_URL,
    NOTES_EDIT_URL_AUTHOR,
)
from notes.forms import NoteForm


class TestContent(BaseTestSetup):

    def test_notes_visibility_in_list(self):
        cases = (
            (self.author_client, self.author_note, True),
            (self.author_client, self.other_note, False),
        )
        for client, note, should_be_in_list in cases:
            with self.subTest(note=note):
                response = client.get(NOTES_LIST_URL)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                if should_be_in_list:
                    self.assertIn(note, response.context['object_list'])
                else:
                    self.assertNotIn(note, response.context['object_list'])

    def test_forms_on_add_and_edit_pages(self):
        urls = (NOTES_ADD_URL, NOTES_EDIT_URL_AUTHOR)
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
