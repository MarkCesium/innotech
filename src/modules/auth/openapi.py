from src.core.schemas import ErrorResponse

UNAUTHORIZED_RESPONSE = {
    401: {
        "model": ErrorResponse,
        "description": "Invalid or expired token",
    }
}
