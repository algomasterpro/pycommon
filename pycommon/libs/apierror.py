class APIErrors(Exception):
    def __init__(self, message, statusCode=None, errors=None):
        super().__init__()
        self.message = message
        if statusCode is not None:
            self.statusCode = statusCode
        self.errors = errors
    
    def serializeErrors(self):
        pass

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        if self.errors is not None:
           rv['errors'] = self.errors
        if self.statusCode is not None:
           rv['statusCode'] = self.statusCode

        return rv

class APIError(Exception):
    """All custom API Exceptions"""
    pass

class ForbiddenError(APIErrors):
    """Custom Authentication Error Class."""
    statusCode = 403
    reason = "Forbidden"

    def serializeErrors(self):
        return [{ "message": self.reason }]

class BadRequestError(APIErrors):
    statusCode = 400
    reason = "Bad request Error"

    def serializeErrors(self):
        return [{ "message": self.reason }]

class UnauthorizedError(APIErrors):
    statusCode = 401
    reason = "Unauthorized"

    def serializeErrors(self):
        return [{ "message": self.reason }]

class NotFoundError(APIErrors):
    statusCode = 404
    reason = "Not found"

    def serializeErrors(self):
        return [{ "message": self.reason }]