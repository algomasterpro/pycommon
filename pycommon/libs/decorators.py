import os
from functools import wraps
from flask import request
import jwt

from ..libs.apierror import UnauthorizedError, APIErrors, ForbiddenError

def token_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = None
            # jwt is passed in the request cookie
            token = request.cookies.get('Authorization')

            if not token:
                raise UnauthorizedError('Token is missing !!')

            try:
                # decoding the payload to fetch the stored details
                data = jwt.decode(token, os.getenv("JWT_KEY"), algorithms=['HS256'])
                if data["authorized"] is False:
                   raise UnauthorizedError('Token is missing !!')
                setattr(request, "currentuser", data)
                return fn(*args, **kwargs)
            except Exception as e:
                if isinstance(e, APIErrors):
                    raise e 
                raise UnauthorizedError('Token is missing !!')

        return decorator

    return wrapper


def perm_check(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            currentuser = request.currentuser
            if not currentuser:
                raise UnauthorizedError('Token is missing !!')

            try:
                  # decoding the payload to fetch the stored details
                if currentuser["role"] in roles is False:
                    raise ForbiddenError('You are not authorized to access this route')
                return fn(*args, **kwargs)
            except Exception as e:
                if isinstance(e, APIErrors):
                    raise e 
                raise ForbiddenError('You are not authorized to access this route')

        return decorator

    return wrapper