from fastapi import HTTPException
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings

client =  TestClient(app, raise_server_exceptions=False)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200
    assert "CampusAssist AI" in response.text


def test_chat_without_api_key():
    response = client.post(
        "/chat",
        json={"question": "What is machine learning?"}
    )

    assert response.status_code == 401


def test_chat_with_invalid_api_key():
    response = client.post(
        "/chat",
        headers={"X-API-Key": "wrong-key"},
        json={"question": "What is machine learning?"}
    )

    assert response.status_code == 401


def test_chat_with_empty_question():
    response = client.post(
        "/chat",
        headers={
    "X-API-Key": settings.API_SECRET_KEY.get_secret_value()},
        json={"question": ""}
    )

    assert response.status_code == 422


def test_chat_with_oversized_question():
    response = client.post(
        "/chat",
        headers={
            "X-API-Key": settings.API_SECRET_KEY.get_secret_value()
        },
        json={"question": "A" * 2001}
    )

    assert response.status_code == 422

def test_chat_with_valid_api_key():
    with patch(
        "app.api.routes.generate_answer",
        new_callable=AsyncMock
    ) as mock_generate:

        mock_generate.return_value = "Machine learning is a type of AI."

        response = client.post(
            "/chat",
            headers={
                "X-API-Key": settings.API_SECRET_KEY.get_secret_value()
            },
            json={"question": "What is machine learning?"}
        )

    assert response.status_code == 200
    assert response.json()["answer"] == "Machine learning is a type of AI."



def test_chat_rate_limiting():
    from app.core.rate_limiter import request_records

    request_records.clear()

    headers = {
        "X-API-Key": settings.API_SECRET_KEY.get_secret_value()
    }

    with patch(
        "app.api.routes.generate_answer",
        new_callable=AsyncMock
    ) as mock_generate:

        mock_generate.return_value = "This is a test response."

        # First 5 requests should succeed
        for _ in range(5):
            response = client.post(
                "/chat",
                headers=headers,
                json={"question": "What is AI?"}
            )

            assert response.status_code == 200

        # Sixth request should be rejected
        response = client.post(
            "/chat",
            headers=headers,
            json={"question": "What is AI?"}
        )

        assert response.status_code == 429


def test_groq_timeout():
    from app.core.rate_limiter import request_records

    # Clear previous rate-limit records
    request_records.clear()

    headers = {
        "X-API-Key": settings.API_SECRET_KEY.get_secret_value()
    }

    with patch(
        "app.api.routes.generate_answer",
        new_callable=AsyncMock
    ) as mock_generate:

        mock_generate.side_effect = HTTPException(
            status_code=504,
            detail="The AI service took too long to respond. Please try again."
        )

        response = client.post(
            "/chat",
            headers=headers,
            json={"question": "Explain artificial intelligence."}
        )

    assert response.status_code == 504


def test_groq_provider_failure():
    from app.core.rate_limiter import request_records

    request_records.clear()

    headers = {
        "X-API-Key": settings.API_SECRET_KEY.get_secret_value()
    }

    with patch(
        "app.api.routes.generate_answer",
        new_callable=AsyncMock
    ) as mock_generate:

        mock_generate.side_effect = HTTPException(
            status_code=502,
            detail="The AI service is temporarily unavailable. Please try again later."
        )

        response = client.post(
            "/chat",
            headers=headers,
            json={"question": "Explain artificial intelligence."}
        )

    assert response.status_code == 502


def test_unexpected_application_error():
    from app.core.rate_limiter import request_records

    request_records.clear()

    headers = {
        "X-API-Key": settings.API_SECRET_KEY.get_secret_value()
    }

    with patch(
        "app.api.routes.generate_answer",
        new_callable=AsyncMock
    ) as mock_generate:

        mock_generate.side_effect = RuntimeError("Simulated internal error")

        response = client.post(
            "/chat",
            headers=headers,
            json={"question": "Explain artificial intelligence."}
        )

    assert response.status_code == 500
    assert response.json()["error"]["type"] == "INTERNAL_SERVER_ERROR"




