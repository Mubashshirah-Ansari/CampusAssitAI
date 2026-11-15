# CampusAssist AI

**An AI-powered university student support assistant built with FastAPI and Groq.**

## 1. Project Overview

CampusAssist AI is a backend application designed to help university students get answers to common questions through an AI-powered chat interface.

The application accepts student questions, validates requests, checks API authentication, applies rate limiting, sends questions to a Large Language Model (LLM) through the Groq API, and returns the generated response.

## 2. Technology Stack

- **Language:** Python
- **Backend framework:** FastAPI
- **AI provider:** Groq
- **Model:** `openai/gpt-oss-20b`
- **Request validation:** Pydantic
- **Configuration:** Environment variables and Pydantic Settings
- **HTTP client:** HTTPX
- **Testing:** Pytest and FastAPI TestClient
- **Frontend:** HTML, CSS and JavaScript
- **Containerization:** Docker (configuration prepared; container testing pending)

## 3. Main Features

- AI-powered student question answering.
- REST API endpoints.
- API-key authentication using the `X-API-Key` header.
- Request validation, including question length limits.
- Rate limiting: 5 requests per client IP within 60 seconds by default.
- Centralized error handling.
- Request IDs for tracking requests.
- Operational logging and response-time measurement.
- Configurable Groq model and timeout.
- Simple web-based chat interface.
- Automated API tests.

## 4. Project Structure

```text
CampusAssistAI/
│
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   └── routes.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── error_handlers.py
│   │   └── rate_limiter.py
│   │
│   ├── services/
│   │   └── groq_service.py
│   │
│   ├── static/
│   │   └── index.html
│   │
│   └── main.py
│
├── tests/
│   └── test_api.py
│
├── docs/
│   ├── architecture.md
│   ├── api_design.md
│   └── submission_report.md
│
├── scripts/
│   └── performance_test.py
│
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## 5. Installation and Setup

### Prerequisites

- Python 3.13
- pip
- A Groq API key
- Git (for version control)
- Docker Desktop (for container execution)

### Step 1: Clone the repository

After the project has been uploaded to GitHub:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd CampusAssistAI
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

Configure these variables:

```env
APP_NAME=CampusAssist AI
ENVIRONMENT=development
API_SECRET_KEY=your_generated_secret
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
GROQ_TIMEOUT_SECONDS=30
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW_SECONDS=60
```

Replace the placeholder values with your own credentials. Never commit or share the `.env` file.

### Step 5: Run the application

```bash
uvicorn app.main:app --reload
```

The application will run locally at:

- Frontend: `http://127.0.0.1:8000/`
- API documentation: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/health`

## 6. API Endpoints

| Endpoint | Method | Purpose | Authentication |
|---|---|---|---|
| `/health` | GET | Checks application health | Not required |
| `/chat` | POST | Generates an AI response | Required |

### Health endpoint

Request:

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "CampusAssist AI"
}
```

### Chat endpoint

Request:

```http
POST /chat
```

Required header:

```http
X-API-Key: YOUR_API_SECRET_KEY
```

Example request body:

```json
{
  "question": "What is machine learning?"
}
```

The question must contain between 1 and 2000 characters.

The response contains the generated answer and request ID.

## 7. Authentication and Security

- API authentication uses a secret key configured through environment variables.
- The application compares API keys using a constant-time comparison function.
- Missing and invalid API keys are rejected.
- API credentials are not hardcoded in the application source.
- `.env` is excluded through `.gitignore` and `.dockerignore`.
- Error responses avoid exposing internal exception details to clients.

**Important:** The current frontend accepts an API key entered by the user. This is suitable for a local academic demonstration, not a production authentication design. A production application should use an appropriate user authentication and session-management system.

## 8. Rate Limiting

The chat endpoint uses a configurable in-memory rate limiter.

Default configuration:

- Maximum requests: 5
- Time window: 60 seconds
- Client identification: Client IP address
- Exceeded response: HTTP 429 Too Many Requests
- Retry information: `Retry-After` response header

**Limitation:** The current rate limiter stores data in application memory. Its records are reset when the application restarts, and separate worker processes do not share the same counters. A distributed production deployment should use shared storage such as Redis.

## 9. LLM Integration

CampusAssist AI uses the Groq API to generate responses.

- Provider: Groq
- Model configured: `openai/gpt-oss-20b`
- Maximum completion tokens: 512
- Request timeout: 30 seconds
- System prompt: Defines the assistant as a helpful university student-support assistant.
- User prompt: Contains the student's submitted question.

The application handles AI service timeouts and provider or connection failures using controlled HTTP error responses.

Token usage and cost depend on actual model usage and the provider's current pricing. No fixed cost is assumed in this project.

## 10. Error Handling

The application provides structured error responses for:

| HTTP status | Meaning |
|---|---|
| 401 | Missing or invalid API key |
| 422 | Invalid or oversized request |
| 429 | Rate limit exceeded |
| 502 | AI provider or connection failure |
| 504 | AI service timeout |
| 500 | Unexpected application error |

Responses include an error type, a safe message and a request ID where available.

## 11. Logging and Monitoring

The backend records:

- Request ID
- HTTP method
- Endpoint path
- Response status
- Request latency
- Unexpected application errors

A performance test was conducted using 20 requests to the `/health` endpoint.

Recorded results:

| Metric | Result |
|---|---:|
| Total requests | 20 |
| Successful requests | 20 |
| Failed requests | 0 |
| Success rate | 100% |
| Error rate | 0% |
| Average response time | 3.53 ms |
| Maximum response time | 35.32 ms |

These measurements apply to the health endpoint test, not to 20 AI-generation requests.

## 12. Automated Testing

Run the automated tests using:

```bash
python -m pytest tests/test_api.py -v
```

Latest recorded test result:

**11 passed, 0 failed.**

The tests cover:

- Health endpoint
- Homepage
- Missing API key
- Invalid API key
- Empty question
- Oversized question
- Successful authenticated chat request
- Rate limiting
- Simulated AI timeout
- Simulated AI provider failure
- Unexpected application error

Some AI failure paths are tested using mocks so that the application can be tested without depending on a live provider failure.

## 13. Docker Instructions

The project includes a `Dockerfile` and `.dockerignore`.

After Docker Desktop is installed and running, build the image:

```bash
docker build -t campusassist-ai .
```

Run the container:

```bash
docker run --rm -p 8000:8000 --env-file .env campusassist-ai
```

Then visit:

```text
http://127.0.0.1:8000/health
```

The Docker build and runtime instructions are provided here. Successful container execution must be verified before reporting Docker as completed.

## 14. Scope and Limitations

- The optional third-party API integration task was intentionally skipped.
- `/external-data` is documented as a planned endpoint but is not implemented.
- The current rate limiter is in-memory and intended for a demonstration environment.
- The frontend API-key input is not a production user-authentication mechanism.
- AI responses depend on the external Groq service and may vary.
- Docker and GitHub deployment must be verified before final submission.

## 15. Project Documentation

Additional documentation is available in the `docs/` directory:

- `architecture.md` – application architecture and request flow.
- `api_design.md` – endpoint contracts and design decisions.
- `submission_report.md` – case study implementation and verification summary.

## 16. Security Reminder

Never upload or share:

- `.env`
- Actual Groq API keys
- Actual API secret keys
- Personal credentials

Share `.env.example` instead, containing placeholder values only.
