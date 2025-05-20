# Job Platform  API

## Introduction

Hire Platform is a job posting and management system built using Django Ninja and Django Ninja JWT for authentication. It provides APIs for creating, retrieving, updating, and deleting job postings, as well as managing user accounts and authentication.

---

## Features

- **Job Management**: 
  - Create, retrieve, update, and delete job postings.
  - Filter and search job postings by various criteria.
  
- **User Management**:
  - User registration and authentication using JWT.
  - Enable or disable user accounts.
  
- **API Documentation**:
  - Automatically generated API documentation using Django Ninja.

---

## Requirements

- Python 3.10+
- Django Ninja
- Pytest
- Docker and Docker Compose
- PostgreSQL (used as the database)

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/daijay/FullStack-homework.git
```

### Build Docker Image
```bash
docker-compose build
```

### Run Docker Image
```bash
docker-compose up
```

### Stop Docker Image
```bash
docker-compose down
```

---

## Usage

### API Documentation
You can view the API documentation at:
```
http://localhost:8000/api/docs
```

### API Endpoints
- **Job Management**:
  - `POST /api/jobs/`: Create a new job posting.
  - `GET /api/jobs/`: Retrieve a list of job postings.
  - `GET /api/jobs/{job_id}/`: Retrieve a specific job posting by ID.
  - `PUT /api/jobs/{job_id}/`: Update a job posting.
  - `DELETE /api/jobs/{job_id}/`: Delete a job posting.

- **User Management**:
  - `POST /api/user/create/`: Register a new user.
  - `POST /api/user/login/`: Authenticate a user and obtain a JWT token.

- **JWT Token**:
  - `POST /api/auth/api-token-refresh/`: Refresh JWT token.


---

## Running Tests

### Run All Tests
```bash
docker-compose run --rm backend sh -c "pytest"
```

### Run Specific Tests
```bash
docker-compose run --rm backend sh -c "pytest tests/hire/test_hire_api.py"
```

---

## Project Structure

```
.
├── backend
│   ├── hire
│   │   ├── models.py       # Job posting models
│   │   ├── views.py        # Job posting views
│   │   ├── api.py          # Job posting API endpoints
│   │   └── tests           # Job posting tests
│   ├── user
│   │   ├── schemas.py      # User schemas
│   │   ├── views.py        # User views
│   │   └── api.py          # User API endpoints
│   └── settings.py         # Django settings
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # Project documentation
```

---

