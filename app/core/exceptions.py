class BaseAppException(Exception):
    """Base class for all application exceptions."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(BaseAppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class UnauthorizedException(BaseAppException):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=401)

class ConflictException(BaseAppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)

class ValidationException(BaseAppException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422)
