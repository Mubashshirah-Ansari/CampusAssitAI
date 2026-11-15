
import secrets

from fastapi import Header, HTTPException, status

from app.core.config import settings


async def verify_api_key(
    api_key: str | None = Header(default=None, alias="X-API-Key")
):
    # Check whether the API key is provided
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing"
        )

    # Check whether the API key is configured in .env
    if settings.API_SECRET_KEY is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API authentication is not configured"
        )

    # Compare the provided key with the secret key
    actual_key = settings.API_SECRET_KEY.get_secret_value()

    if not secrets.compare_digest(api_key, actual_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    return True
