import uuid


class AppError(Exception):
    """Base application error."""

    def __init__(
        self, message: str, code: str = "UNEXPECTED_ERROR", correlation_id: str = None
    ):
        self.message = message
        self.code = code
        self.correlation_id = correlation_id if correlation_id else str(uuid.uuid4())
        super().__init__(self.message)


class NotFoundError(AppError):
    """Resource not found."""

    def __init__(self, resource: str, correlation_id: str = None):
        super().__init__(
            message=f"{resource} not found",
            code="NOT_FOUND",
            correlation_id=correlation_id,
        )


class ForbiddenError(AppError):
    """User is not authorized to perform action."""

    def __init__(
        self, message: str = "Not enough permissions", correlation_id: str = None
    ):
        super().__init__(
            message=message, code="FORBIDDEN", correlation_id=correlation_id
        )


class ConflictError(AppError):
    """Resource conflict, e.g., duplicate email."""

    def __init__(self, message: str, correlation_id: str = None):
        super().__init__(
            message=message, code="CONFLICT", correlation_id=correlation_id
        )
