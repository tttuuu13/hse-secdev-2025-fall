class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, code: str = "UNEXPECTED_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundError(AppError):
    """Resource not found."""

    def __init__(self, resource: str):
        super().__init__(message=f"{resource} not found", code="NOT_FOUND")


class ForbiddenError(AppError):
    """User is not authorized to perform action."""

    def __init__(self, message: str = "Not enough permissions"):
        super().__init__(message=message, code="FORBIDDEN")


class ConflictError(AppError):
    """Resource conflict, e.g., duplicate email."""

    def __init__(self, message: str):
        super().__init__(message=message, code="CONFLICT")
