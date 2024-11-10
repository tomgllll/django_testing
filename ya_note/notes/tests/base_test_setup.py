from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

AUTHOR_SLUG = 'author_slug'
OTHER_USER_SLUG = 'other_user_slug'

AUTHOR_TITLE = 'Заметка Автора'
AUTHOR_TEXT = 'Текст заметки автора'
NEW_AUTHOR_TEXT = 'Обновленный текст заметки'

HOMEPAGE_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
NOTES_LIST_URL = reverse('notes:list')
NOTES_ADD_URL = reverse('notes:add')
NOTES_DETAIL_URL = reverse('notes:detail', args=[AUTHOR_SLUG])
NOTES_EDIT_URL_AUTHOR = reverse('notes:edit', args=[AUTHOR_SLUG])
NOTES_EDIT_URL_OTHER = reverse('notes:edit', args=[OTHER_USER_SLUG])
NOTES_DELETE_URL_AUTHOR = reverse('notes:delete', args=[AUTHOR_SLUG])
NOTES_DELETE_URL_OTHER = reverse('notes:delete', args=[OTHER_USER_SLUG])
NOTES_SUCCESS = reverse('notes:success')


class BaseTestSetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.other_user = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title=AUTHOR_TITLE,
            text=AUTHOR_TEXT,
            slug=AUTHOR_SLUG,
            author=cls.author
        )
        cls.author_client = cls.client_class()
        cls.author_client.force_login(cls.author)

        cls.other_user_client = cls.client_class()
        cls.other_user_client.force_login(cls.other_user)

        cls.form_data = {'title': AUTHOR_TITLE,
                         'text': NEW_AUTHOR_TEXT}
