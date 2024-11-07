import pytest
from django.test.client import Client
from django.urls import reverse
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def comment(author, news_item):
    return Comment.objects.create(news=news_item, author=author, text='Текст')


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='author_user')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def news_item(author):
    return News.objects.create(title='Test News', text='Sample text')


@pytest.fixture
def not_author_user(django_user_model):
    return django_user_model.objects.create(username='another_user')


@pytest.fixture
def not_author_client(not_author_user):
    client = Client()
    client.force_login(not_author_user)
    return client


@pytest.fixture
def pk_for_args(comment):
    return (comment.pk,)


@pytest.fixture
def comment_form_data():
    return {'text': 'Текст комментария'}


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news_item):
    return reverse('news:detail', args=(news_item.id,))


@pytest.fixture
def setup_news():
    today = datetime.today()
    all_news = [
        News(
            title='Новость',
            text='текст',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def setup_comments(news_item, author):
    now = timezone.now()
    comments = [
        Comment(
            news=news_item,
            author=author,
            text=f'Tекст {index}',
            created=now + timedelta(days=index)
        ) for index in range(10)
    ]
    Comment.objects.bulk_create(comments)