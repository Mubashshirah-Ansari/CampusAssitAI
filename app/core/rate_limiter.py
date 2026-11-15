
import time
from threading import Lock

from fastapi import Request, HTTPException, status

from app.core.config import settings


# Store request timestamps for each client
request_records = {}

# Prevent simultaneous requests from modifying records at once
lock = Lock()


def check_rate_limit(request: Request):
    client_ip = request.client.host if request.client else "unknown"

    current_time = time.monotonic()

    limit = settings.RATE_LIMIT_REQUESTS
    window = settings.RATE_LIMIT_WINDOW_SECONDS

    with lock:
        # Get timestamps for this client
        timestamps = request_records.get(client_ip, [])

        # Remove timestamps outside the time window
        timestamps = [
            timestamp
            for timestamp in timestamps
            if current_time - timestamp < window
        ]

        # Check whether the client has exceeded the limit
        if len(timestamps) >= limit:
            retry_after = max(
                1,
                int(window - (current_time - timestamps[0]))
            )

            request_records[client_ip] = timestamps

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
                headers={"Retry-After": str(retry_after)}
            )

        # Record this request
        timestamps.append(current_time)
        request_records[client_ip] = timestamps

    return True
