# CampusAssist AI – Final Case Study Report

## 1. Introduction

CampusAssist AI is an AI-powered university student support application developed using Python, FastAPI and the Groq API.

The purpose of the project is to provide students with an interface through which they can ask questions and receive AI-generated responses.

The project focuses on backend development, API design, authentication, rate limiting, error handling, LLM integration, logging, monitoring and automated testing.

## 2. Implementation Summary

| Task | Description | Status |
|---|---|---|
| Task 1 | Architecture design | Completed |
| Task 2 | API design | Completed |
| Task 3 | Backend implementation | Completed |
| Task 4 | LLM integration | Implemented |
| Task 5 | Third-party API integration | Skipped – optional task |
| Task 6 | Authentication and secret management | Implemented and tested |
| Task 7 | Rate limiting | Implemented and tested |
| Task 8 | Error handling | Implemented and tested |
| Task 9 | Logging, monitoring and frontend UI | Implemented and tested |
| Task 10 | Docker containerization | Configuration prepared; testing pending |
| Task 11 | Git version control | Git installed; repository setup and commits pending |
| Task 12 | Automated testing | Completed |

## 3. Architecture

The application follows a modular backend architecture.

The main request flow is:

1. A student submits a question through the frontend or API.
2. FastAPI receives the request.
3. The application assigns a request ID and records request information.
4. Authentication verifies the API key.
5. Rate limiting checks the client's request count.
6. Pydantic validates the request.
7. The API route calls the Groq service.
8. Groq generates an AI response.
9. FastAPI returns the response to the student.

Centralized error handlers provide controlled responses when requests or services fail.

Refer to `architecture.md` for the architecture diagram.

## 4. API Design

The implemented endpoints are:

### GET /health

Checks whether the application is running.

### POST /chat

Accepts an authenticated student question and returns an AI-generated response.

Authentication is performed using the `X-API-Key` header.

The optional `/external-data` endpoint was documented but not implemented because the third-party API task was skipped.

Refer to `api_design.md` for the endpoint contracts.

## 5. LLM Integration

The application integrates with Groq using the configured model:

`openai/gpt-oss-20b`

A system prompt defines the assistant's role as a helpful university student-support assistant.

The integration includes:

- Configurable model selection.
- Maximum completion token limit of 512.
- Configurable timeout of 30 seconds.
- Handling for provider and connection failures.
- Handling for request timeouts.

## 6. Security

The application uses environment variables for secret configuration.

Security measures include:

- API-key authentication.
- Constant-time API-key comparison.
- Missing and invalid credential rejection.
- Exclusion of `.env` from Git and Docker build contexts.
- Safe error messages for unexpected failures.

The actual API keys are not included in this report or the source repository.

## 7. Rate Limiting

The default rate limit is five requests per client IP within a 60-second window.

When the limit is exceeded, the application returns HTTP 429 and a `Retry-After` header.

The implementation uses in-memory storage and is intended for the academic demonstration. It does not provide shared rate-limit state across multiple application workers.

## 8. Error Handling

The application handles the following scenarios:

- Missing or invalid API key.
- Invalid request data.
- Oversized questions.
- Rate-limit violations.
- AI provider failures.
- AI service timeouts.
- Unexpected application errors.

The error responses use consistent structures and request IDs where available.

## 9. Logging and Performance Testing

The application logs request IDs, HTTP methods, endpoint paths, response statuses and request latency.

A performance test was conducted using 20 requests to the health endpoint.

### Recorded performance results

| Metric | Result |
|---|---:|
| Total requests | 20 |
| Successful requests | 20 |
| Failed requests | 0 |
| Success rate | 100% |
| Error rate | 0% |
| Average response time | 3.53 ms |
| Maximum response time | 35.32 ms |

These results represent health endpoint testing, not AI-generation performance.

## 10. Frontend

A simple web interface was developed using HTML, CSS and JavaScript.

It includes:

- API-key input.
- Student question input.
- Send button.
- Loading indicator.
- AI response display.
- Controlled error messages.

The frontend was tested with a real request to the Groq service.

## 11. Automated Testing

Automated tests were implemented using Pytest and FastAPI TestClient.

The latest recorded result:

**11 tests passed and 0 tests failed.**

The test suite covers:

1. Health endpoint.
2. Homepage.
3. Missing API key.
4. Invalid API key.
5. Empty question.
6. Oversized question.
7. Successful authenticated chat request.
8. Rate limiting.
9. Simulated AI timeout.
10. Simulated AI provider failure.
11. Unexpected application error.

## 12. Docker and Version Control

### Task 10 – Docker

**Status: Completed and tested**

- Created a Dockerfile for CampusAssist AI.
- Created `.dockerignore` to exclude unnecessary files and secrets.
- Built the Docker image successfully using `docker build`.
- Ran the application inside a Docker container.
- Verified the `/health` endpoint successfully.
- Verified that the frontend loads through the Docker container.
- Environment variables are supplied locally using `--env-file .env`.

## 13. Limitations and Future Improvements

Potential improvements include:

- Implementing the optional third-party API integration.
- Using Redis for distributed rate limiting.
- Adding production-grade student authentication.
- Adding persistent conversation history.
- Improving monitoring and operational metrics.
- Completing Docker deployment verification.
- Publishing the source code through GitHub.

## 14. Conclusion

CampusAssist AI demonstrates the development of an AI-powered backend application using FastAPI and Groq.

The project implements API authentication, request validation, rate limiting, LLM integration, centralized error handling, logging, a frontend interface and automated tests.

The latest automated test run completed successfully with 11 passing tests and no failures.

Docker and GitHub completion will be recorded after their respective build, runtime and repository checks have been successfully verified.

## 15. Submission Details

**Project:** CampusAssist AI

**Student Roll Number:** [DS2502]

**Technology:** Python, FastAPI, Groq and Docker

**Automated Test Result:** 11 passed, 0 failed

