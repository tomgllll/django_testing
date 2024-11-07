import pytest

from http import HTTPStatus
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_user_can_create_comment(author_client,
                                 author,
                                 news_item,
                                 comment_form_data):
    url = reverse('news:detail', args=(news_item.id,))
    response = author_client.post(url, data=comment_form_data)
    assert response.status_code == HTTPStatus.FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == comment_form_data['text']
    assert comment.news == news_item
    assert comment.author == author


def test_anonymous_user_cant_create_comment(client,
                                            news_item,
                                            comment_form_data):
    url = reverse('news:detail', args=(news_item.id,))
    client.post(url, data=comment_form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_use_bad_words(author_client, news_item):
    url = reverse('news:detail', args=(news_item.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assert WARNING in response.context['form'].errors['text']
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, comment):
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('news:detail',
                                   args=(comment.news.id,)) + '#comments'
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(not_author_client, comment):
    delete_url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, comment, comment_form_data):
    edit_url = reverse('news:edit', args=(comment.id,))
    comment_form_data['text'] = 'Обновленный текст'
    response = author_client.post(edit_url, data=comment_form_data)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('news:detail',
                                   args=(comment.news.id,)) + '#comments'
    comment.refresh_from_db()
    assert comment.text == 'Обновленный текст'


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(not_author_client,
                                                comment,
                                                comment_form_data):
    edit_url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(edit_url, data=comment_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment.text
