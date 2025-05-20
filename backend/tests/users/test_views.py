import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from backend.tests.test_utils import get_authentication_header


@pytest.mark.django_db
class TestUserView:
    def test_create_new_user_should_pass(self, random_email, random_username, client):
        url = reverse("hireplatform:user-create")
        print(url)
        payload = {
            "username": random_username,
            "email": random_email,
            "password": "password",
            "first_name": "test",
            "last_name": "test",
        }
        response = client.post(
            url, payload, format="json", content_type="application/json"
        )

        assert response.status_code == 201
        assert response.json()["token"]

    def test_create_new_user_with_existing_email_should_fail(
        self, random_email, random_username, client
    ):
        url = reverse("hireplatform:user-create")
        payload = {
            "username": random_username,
            "email": random_email,
            "password": "password",
            "first_name": "test",
            "last_name": "test",
        }
        response = client.post(
            url, payload, format="json", content_type="application/json"
        )
        assert response.status_code == 201

        response = client.post(url, payload, format="json")
        assert response.status_code == 400


    def test_delete_user_success(self, app_admin, user, client):
        headers = get_authentication_header(app_admin, header_key="HTTP_AUTHORIZATION")

        url = reverse("hireplatform:user-delete", kwargs={"pk": user.id})
        response = client.delete(url, format="json", **headers)
        assert response.status_code == 200

        user = User.objects.filter(pk=user.pk).first()
        assert user is None
