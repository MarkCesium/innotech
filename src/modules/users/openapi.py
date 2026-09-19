from src.core.schemas import ErrorResponse

USER_ALREADY_EXISTS_RESPONSE = {
    409: {
        "model": ErrorResponse,
        "description": "User with this email already exists",
    }
}

USER_ALREADY_ACTIVATED_OR_NOT_FOUND_RESPONSE = {
    400: {
        "model": ErrorResponse,
        "description": "User already activated or not found",
    }
}
