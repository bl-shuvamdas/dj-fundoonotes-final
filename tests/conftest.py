import pytest  # noqa
from rest_framework.reverse import reverse

from note.models import Note


@pytest.fixture
def user_data():
    return {"username": 'admin', "email": 'admin@email.com', "password": 'password',
            'is_verify': True}


@pytest.fixture
def user_obj(db, django_user_model, user_data):
    return django_user_model.objects.create_user(**user_data)


@pytest.fixture
def note_data(user_obj, db):
    return {"title": 'test title', "description": 'test description.', 'user': user_obj}


@pytest.fixture
def note_obj(db, note_data):
    return Note.objects.create(**note_data)  # noqa


@pytest.fixture
def headers(db, client, user_obj):
    payload = {"username": 'admin', "password": 'password'}
    response = client.post(reverse('auth:login'), payload)
    token = response.data['data']['token']
    return {'content_type': 'application/json', 'HTTP_TOKEN': token}
