import pytest
from django.urls import reverse

from backend.tests.test_utils import get_authentication_header


@pytest.mark.django_db
class TestHireView:
    def test_create_job_should_pass(self, client, app_admin, job_payload):
        """Test successfully creating a job"""
        headers = get_authentication_header(app_admin, header_key="HTTP_AUTHORIZATION")
        url = reverse("hireplatform:create_job")
        response = client.post(url, job_payload, format="json", content_type="application/json", **headers)
        assert response.status_code == 201
        assert response.json()["title"] == "Software Engineer"

    def test_create_job_with_missing_fields_should_fail(self, client, app_admin, job_payload):
        """Test failing to create a job due to missing required fields"""
        headers = get_authentication_header(app_admin, header_key="HTTP_AUTHORIZATION")
        url = reverse("hireplatform:create_job")
        # Remove required field
        del job_payload["description"]
        response = client.post(url, job_payload, format="json", content_type="application/json", **headers)
        assert response.status_code == 422

    def test_get_job_list_should_pass(self, client, app_admin):
        """Test successfully retrieving the job list"""
        headers = get_authentication_header(app_admin, header_key="HTTP_AUTHORIZATION")
        url = reverse("hireplatform:get_jobs")
        response = client.get(url, format="json", **headers)
        assert response.status_code == 200
        assert isinstance(response.json()["items"], list)

    def test_get_job_by_id_should_pass(self, client, app_admin, create_job):
        """Test successfully retrieving a job by ID"""
        headers = get_authentication_header(app_admin, header_key="HTTP_AUTHORIZATION")
        job_id = create_job.job_id
        url = reverse("hireplatform:get_job", kwargs={"job_id": job_id})
        response = client.get(url, format="json", **headers)
        assert response.status_code == 200
        assert response.json()["job_id"] == job_id

    def test_update_job_should_pass(self, client, app_admin, create_job, job_payload):
        """Test successfully updating a job"""
        headers = get_authentication_header(app_admin, header_key="HTTP_AUTHORIZATION")
        job_id = create_job.job_id
        url = reverse("hireplatform:update_job", kwargs={"job_id": job_id})
        # Update fields in the payload
        job_payload["title"] = "Senior Software Engineer"
        job_payload["description"] = "Lead and maintain software projects."
        job_payload["location"] = "Onsite"
        job_payload["salary_range"] = "$80,000 - $100,000"
        response = client.put(url, job_payload, format="json", content_type="application/json", **headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Senior Software Engineer"

    def test_update_job_with_missing_fields_should_fail(self, client, app_admin, create_job, job_payload):
        """Test failing to update a job due to missing required fields"""
        headers = get_authentication_header(app_admin, header_key="HTTP_AUTHORIZATION")
        job_id = create_job.job_id
        url = reverse("hireplatform:update_job", kwargs={"job_id": job_id})
        # Remove required field
        del job_payload["title"]
        response = client.put(url, job_payload, format="json", content_type="application/json", **headers)
        assert response.status_code == 422

    def test_delete_job_should_pass(self, client, app_admin, create_job):
        """Test successfully deleting a job"""
        headers = get_authentication_header(app_admin, header_key="HTTP_AUTHORIZATION")
        job_id = create_job.job_id
        url = reverse("hireplatform:delete_job", kwargs={"delete_id": job_id})
        print(url)
        response = client.delete(url, format="json", content_type="application/json", **headers)
        assert response.status_code == 200
        
    def test_delete_job_not_found_should_fail(self, client, app_admin):
        """Test deleting a non-existent job should fail"""
        headers = get_authentication_header(app_admin, header_key="HTTP_AUTHORIZATION")
        non_existent_job_id = 999999
        url = reverse("hireplatform:delete_job", kwargs={"delete_id": non_existent_job_id})
        response = client.delete(url, format="json", content_type="application/json", **headers)
        assert response.status_code == 404