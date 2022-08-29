import pytest  # noqa
from rest_framework.reverse import reverse

REGISTER_URL = reverse('auth:register')
LOGIN_URL = reverse('auth:login')


# Create your tests here.
class TestAuthApi:
    @pytest.mark.parametrize(
        ('payload', 'status'),
        [
            ({'username': 'admin', 'email': 'admin@email.com', 'password': 'password'}, 201),
            ({'username': '', 'email': 'admin@email.com', 'password': 'password'}, 400),
            ({'username': '', 'email': '', 'password': 'password'}, 400),
            ({'username': '', 'email': '', 'password': ''}, 400),
        ])
    def test_register_api_with_credentials(self, db, client, payload, status):
        response = client.post(REGISTER_URL, payload, content_type='application/json')
        assert response.status_code == status

    def test_password_saved_as_hash_format(self, db, django_user_model, user_data):
        user = django_user_model.objects.create_user(**user_data)
        assert user.check_password(user_data['password'])

    def test_password_not_in_register_api_response(self, db, client, user_data):
        response = client.post(REGISTER_URL, user_data, content_type='application/json')
        assert 'password' not in response.data['data']

    @pytest.mark.parametrize(
        ('payload', 'status'),
        [
            ({'username': 'admin', 'password': 'password'}, 200),
            ({'username': '', 'password': ''}, 400),
            ({'username': '', 'password': 'password'}, 400),
            ({'username': 'admin', 'password': ''}, 400),
            ({'username': 'com', 'password': ''}, 400),
        ])
    def test_login_api_with_credentials(self, db, client, django_user_model, user_data, payload, status):
        django_user_model.objects.create_user(**user_data)
        response = client.post(LOGIN_URL, payload, content_type='application/json')
        assert response.status_code == status
