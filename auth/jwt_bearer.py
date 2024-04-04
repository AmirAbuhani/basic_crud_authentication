# This aim of this class is checked whether the request is authorized or not[verification of the protected route]
import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    # This function validates the incoming HTTP request to ensure it contains a valid Bearer token
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid or Expired Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or Expired Token")

    # This function takes a JWT token string (jwtoken) and attempts to decode it using a decodeJWT function
    def verify_jwt(self, jwtoken: str):
        try:
            payload = decodeJWT(jwtoken)
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token has expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=403, detail="Invalid token")
