import os
from functools import wraps
from flask import Flask, request, jsonify, make_response
import jwt

from libs.apierror import BadRequestError, UnauthorizedError 

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        name = request.cookies.get('Authorization')
        # return 401 if token is not passed
        if not name:
            # return jsonify({'message' : 'Token is missing !!'}), 401
            raise UnauthorizedError("Token is missing")
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, os.getenv("JWT_KEY"))
            if data.authorized is False:
                raise UnauthorizedError("Token is missing")
        except:
            raise UnauthorizedError("Token is missing")
        # returns the current logged in users contex to the routes
        return  f(data, *args, **kwargs)
  
    return decorated