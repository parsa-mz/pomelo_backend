from datetime import datetime

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from apps.users.models import User
from core.dependencies.database import database
from core.settings import settings

bearer_scheme = HTTPBearer()


class AuthMiddleware:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY

    def __decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    def generate_token(self, data: dict) -> str:
        # data["iat"] = int(datetime.utcnow().timestamp())
        data["exp"] = int(datetime.utcnow().timestamp() + settings.JWT_ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)
        return jwt.encode(data, self.secret_key, algorithm="HS256")

    def __call__(self, token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
        try:
            payload = self.__decode_token(token.credentials)
            # print("payload", payload)

            # if expired, raise HTTPException
            if payload["exp"] < int(datetime.utcnow().timestamp()):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

            try:
                query = User.select().where(User.c.id == payload["user_id"])
                result = database.execute(query).fetchall()
                user = result[0]
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

            return user

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


auth_middleware = AuthMiddleware()
