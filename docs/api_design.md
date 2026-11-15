
# CampusAssist AI - API Design

## 1. Introduction

This document defines the API contracts for CampusAssist AI.

The backend uses FastAPI to expose REST APIs.

## 2. API Endpoints

### API 1: Health Check

- Endpoint: /health
- Method: GET
- Purpose: Check backend availability.
- Authentication: Not required.
- Request: No request body.

Response:
{
  "status": "healthy",
  "service": "CampusAssist AI"
}

Possible Errors:
- 500: Internal server error.

### API 2: AI Chat

- Endpoint: /chat
- Method: POST
- Purpose: Accept a student question and generate
  an AI response using Groq.
- Authentication: Required using X-API-Key header.

Request Headers:
- X-API-Key: Secret API key.
- Content-Type: application/json.

Request Body:
{
  "question": "What is machine learning?"
}

Response:
{
  "answer": "Machine learning is a branch of AI...",
  "request_id": "generated-request-id"
}

Possible Errors:
- 401: Missing or invalid API key.
- 422: Invalid request.
- 429: Rate limit exceeded.
- 502: LLM provider failure.
- 504: LLM timeout.
- 500: Unexpected server error.

Input Constraints:
- Question must not be empty.
- Maximum question length: 2000 characters.
- Only valid JSON requests are accepted.

### API 3: External Data

- Endpoint: /external-data
- Method: GET
- Purpose: Intended for retrieving information
  from a third-party API.
- Authentication: Planned.
- Implementation: Skipped because the optional
  third-party API task is out of scope.

## 3. API Design Justification

1. GET is used for health checks because it retrieves
   information without modifying server data.

2. POST is used for AI chat because the user submits
   question data in the request body.

3. API key authentication protects the AI endpoint.

4. Pydantic validation ensures valid request data.

5. Appropriate HTTP status codes communicate errors.

6. Request IDs support debugging and monitoring.

## 4. Security Considerations

- API keys are stored in environment variables.
- Secrets are never hard-coded.
- Secrets are never returned in API responses.
- Protected endpoints require authentication.
