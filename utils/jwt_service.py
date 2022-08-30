from datetime import timedelta, datetime
from typing import Union

import jwt
from django.conf import settings
from jwt.exceptions import PyJWTError


class JWT:
    __config = settings.PY_JWT

    @classmethod
    def encode(cls, payload: dict, exp: Union[None, timedelta] = None) -> str:
        if not exp:
            exp = cls.__config['EXP']
        exp = datetime.utcnow() + exp
        payload.update(exp=exp)
        return jwt.encode(payload=payload, key=cls.__config['KEY'], algorithm=cls.__config['ALGORITHM'])

    @classmethod
    def decode(cls, token: str) -> dict:
        try:
            return jwt.decode(jwt=token, key=cls.__config['KEY'], algorithms=[cls.__config['ALGORITHM']])
        except PyJWTError as e:
            raise e
