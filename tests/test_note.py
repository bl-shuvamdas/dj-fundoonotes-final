import pytest  # noqa
from django.forms import model_to_dict
from rest_framework.reverse import reverse

from note.models import Note

# Create your tests here.
NOTE_URL = reverse('note:note_detail')


class TestNoteAPI:
    @pytest.mark.parametrize(('payload', 'status'), [
        ({'title': 'test title', 'description': 'desc.', 'user': True}, 201),
        ({'title': '', 'description': 'desc.', 'user': True}, 400),
        ({'title': 'test title', 'description': '', 'user': True}, 400),
        ({'title': 'test title', 'description': '', 'user': False}, 400),
        ({'title': '', 'description': '', 'user': False}, 400),
    ])
    def test_note_create_api(self, client, db, user_obj, payload, status, headers):
        if payload['user']:
            payload.update(user=user_obj.id)
        response = client.post(NOTE_URL, payload, **headers)
        assert response.status_code == status

    def test_get_note_api_with_user_id(self, client, db, user_obj, headers):
        response = client.get(NOTE_URL, {'user': user_obj.id}, **headers)
        assert response.status_code == 200

    def test_get_note_api_without_user_id(self, client, db, headers):
        response = client.get(NOTE_URL, **headers)
        assert response.status_code == 400

    def test_update_note_api(self, client, db, note_obj, headers):
        prev_data = model_to_dict(note_obj)
        payload = {"id": note_obj.id, 'title': 'new title', 'description': 'new desc.'}
        response = client.put(NOTE_URL, payload, **headers)
        assert response.status_code == 202
        assert response.data['data'] != prev_data

    def test_delete_note_api(self, client, db, note_obj, headers):
        response = client.delete(NOTE_URL, {'id': note_obj.id}, **headers)
        assert Note.objects.count() == 0  # noqa
        assert response.status_code == 204
