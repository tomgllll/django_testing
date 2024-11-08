from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import WARNING
from news.models import Comment


def test_user_can_create_comment(author_client,
                                 author,
                                 news_item,
                                 comment_form_data,
                                 detail_url):
    author_client.post(detail_url, data=comment_form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == comment_form_data['text']
    assert comment.news == news_item
    assert comment.author == author


def test_anonymous_user_cant_create_comment(client,
                                            comment_form_data,
                                            detail_url):
    client.post(detail_url, data=comment_form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_use_bad_words(author_client, detail_url, bad_words_data):
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(response, 'form', 'text', WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, delete_url, detail_url):
    response = author_client.delete(delete_url)
    assertRedirects(response, detail_url + '#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(not_author_client,
                                                  delete_url):
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(author_client, edit_url, comment,
                                 comment_form_data, detail_url):
    original_author = comment.author
    original_news = comment.news
    original_created = comment.created
    comment_form_data['text'] = 'Обновленный текст'
    response = author_client.post(edit_url, data=comment_form_data)
    assertRedirects(response, detail_url + '#comments')
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == 'Обновленный текст'
    assert updated_comment.author == original_author
    assert updated_comment.news == original_news
    assert updated_comment.created == original_created


def test_user_cant_edit_comment_of_another_user(not_author_client,
                                                edit_url,
                                                comment,
                                                comment_form_data):
    original_text = comment.text
    response = not_author_client.post(edit_url, data=comment_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    unchanged_comment = Comment.objects.get(id=comment.id)
    assert unchanged_comment.text == original_text
