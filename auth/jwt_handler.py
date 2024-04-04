# This file is responsible for signing, encoding, decoding and return JWTs
import time
import jwt
from decouple import config

# This is the secret key used for signing and verifying the JWTs
SECRET_KEY = config("SECRET_KEY", default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
# Specifies the algorithm used for encoding and decoding the JWTs
ALGORITHM = "HS256"
# Specifies the expiration time (in minutes) for the access token
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# returns the generated Tokens (JWTs)
def token_response(token: str):
    return {
        "access token": token
    }


# This function takes a username and role as input and generates a JWT with a payload containing the username, role,
# and expiration time
def signJWT(username: str, role: str):
    payload = {
        "username": username,
        # user's role
        "role": role,
        "expiry": time.time() + ACCESS_TOKEN_EXPIRE_MINUTES
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_response(token)


# This function takes a token string as input and attempts to decode it using the jwt.decode function with the
# provided SECRET_KEY and ALGORITHM
def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}
