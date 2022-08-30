from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from utils import JWT


def verify_token(function):
    def wrapper(*args, **kwargs):
        request = list(filter(lambda x: isinstance(x, Request), args))[0]
        if 'Token' not in request.headers:
            raise ValidationError('Unauthorised access')
        payload = JWT.decode(request.headers['Token'])
        if 'user_id' not in payload:
            raise ValidationError('Invalid token used')
        request.data.update(user=payload['user_id'])
        return function(*args, **kwargs)

    return wrapper
