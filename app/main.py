from pathlib import Path
from fastapi.responses import FileResponse
import logging
import time
import uuid

from fastapi import FastAPI, Request

from app.core.config import settings
from app.core.error_handlers import register_exception_handlers
from app.api.routes import router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Campus Assistance Backend",
    version="1.0.0"
)
# Frontend directory
STATIC_DIR = Path(__file__).parent / "static"


# Display the frontend
@app.get("/")
async def home():
    return FileResponse(STATIC_DIR / "index.html")


# Register centralized error handlers
register_exception_handlers(app)


# Request ID and logging middleware
@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        latency = (time.perf_counter() - start_time) * 1000

        logger.info(
            "Request ID: %s | Method: %s | Path: %s | Status: %s | Latency: %.2f ms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            latency
        )

        return response

    except Exception:
        latency = (time.perf_counter() - start_time) * 1000

        logger.exception(
            "Request ID: %s | Method: %s | Path: %s | Error | Latency: %.2f ms",
            request_id,
            request.method,
            request.url.path,
            latency
        )
        raise


# Connect API routes
app.include_router(router)
