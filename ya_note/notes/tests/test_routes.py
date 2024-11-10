from http import HTTPStatus

from .base_test_setup import (
    BaseTestSetup,
    HOMEPAGE_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
    NOTES_LIST_URL,
    NOTES_ADD_URL,
    NOTES_EDIT_URL_AUTHOR,
    NOTES_DELETE_URL_AUTHOR,
    NOTES_SUCCESS,
    NOTES_DETAIL_URL)


class TestRoutes(BaseTestSetup):

    def test_pages_availability(self):
        urls = (HOMEPAGE_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL)
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_note_pages_availability(self):
        user_statuses = (
            (self.author_client, self.note, HTTPStatus.OK),
            (self.other_user_client, self.note, HTTPStatus.NOT_FOUND),
        )
        for user, note, status in user_statuses:
            for url in (NOTES_DETAIL_URL, NOTES_EDIT_URL_AUTHOR,
                        NOTES_DELETE_URL_AUTHOR):
                with self.subTest(user=user, url=url, note=note):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        for url in (
            NOTES_LIST_URL,
            NOTES_SUCCESS,
            NOTES_ADD_URL,
            NOTES_DETAIL_URL,
            NOTES_EDIT_URL_AUTHOR,
            NOTES_DELETE_URL_AUTHOR
        ):
            with self.subTest(url=url):
                redirect_url = f'{LOGIN_URL}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_pages_access_for_authenticated_user(self):
        self.client.force_login(self.author)
        urls = (NOTES_LIST_URL, NOTES_SUCCESS, NOTES_ADD_URL)
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
