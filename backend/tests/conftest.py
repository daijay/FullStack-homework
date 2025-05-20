from datetime import datetime
from random import random

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.utils.timezone import make_aware


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def app_admin():
    user = User.objects.create_user(
        username="admin", email="admin@dmin.com", password="password", is_superuser=True, is_staff=True
    )
    return user


@pytest.fixture
def random_email():
    return "email{}@email.com".format(random())


@pytest.fixture
def random_username():
    return "username{}".format(random())



@pytest.fixture
def user():
    return User.objects.create_user(username="user", email="user@example.com", password="password")



@pytest.fixture
def create_job(db):
    from hire.models import jobs_post
    """
    Creates and returns a job posting for testing purposes.
    """
    return jobs_post.objects.create(
        job_id=21,
        title="Software Engineer",
        description="Develop and maintain software.",
        location="Remote",
        salary_range="$60,000 - $80,000",
        company_name="Tech Company",
        P_date=make_aware(datetime(2025, 5, 16)),
        E_date=make_aware(datetime(2025, 6, 16)),
        skills=["Python", "Django"],
    )

@pytest.fixture
def job_payload():
    """
    Returns a default payload for creating a job posting.
    """
    return {
        "job_id": 1,
        "title": "Software Engineer",
        "description": "Develop and maintain software.",
        "location": "Remote",
        "salary_range": "$60,000 - $80,000",
        "company_name": "Tech Company",
        "P_date": make_aware(datetime(2025, 5, 16)),
        "E_date": make_aware(datetime(2025, 6, 16)),
        "skills": ["Python", "Django"],
    }
