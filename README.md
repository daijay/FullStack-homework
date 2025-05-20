# Job Platform  API

## Introduction

Job Platform API is a job posting and management system built using Django Ninja and Django Ninja JWT for authentication. It provides APIs for creating, retrieving, updating, and deleting job postings, as well as managing user accounts and authentication.

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
  - `POST /api/jobs`: Create a new job posting.
  - `GET /api/jobs`: Retrieve a list of job postings.
  - `GET /api/jobs/{job_id}`: Retrieve a specific job posting by ID.
  - `PUT /api/jobs/{job_id}`: Update a job posting.(without company name)
  - `DELETE /api/jobs/{job_id}/delete`: Delete a job posting.

- **User Management**:
  - `POST /api/user/create`: Register a new user and obtain a JWT token.
  - `POST /api/user/login`: Authenticate a user and obtain a JWT token.

- **JWT Token**:
  - `POST /api/auth/api-token-refresh`: Refresh JWT token.


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

## Design Decisions

1. **Authentication**:
   - 使用 ninja-jwt 作為身分驗證，token type使用sliding token，原因是sliding token較Access token來說更為便捷，且由於沒有設計blacklist，所以不影響效能。

2. **Database**:
   - 使用 PostgreSQL 作為資料庫，原因是其在可靠性、性能和與 Django 的兼容性方面表現優異，也讓未來的擴展提供了更多靈活性。

3. **Testing**:
   - 使用`pytest` and `pytest-django` 撰寫測試，測試涵蓋job和user的create、update、delete等，在後端service 啟動前也會自動做測試。

4. **Docker**:
   - 使用 Docker 將應用程式容器化，這使得應用的設置和部署更加簡單。通過 Docker Compose，可以輕鬆啟動多個服務，並確保開發環境與生產環境的一致性。

---



