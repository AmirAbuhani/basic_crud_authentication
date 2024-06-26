import json

import bcrypt
from fastapi import Depends, HTTPException

from auth import jwt_bearer
from auth.jwt_bearer import jwtBearer
from read_write_users_db import read_users
from models.users_model import UserLoginSchema
from passlib.context import CryptContext

# def hashed_password(password):
#     # Convert the password string to bytes using UTF-8 encoding
#     password_bytes = password.encode('utf-8')
#     # Adding the salt to password
#     salt = bcrypt.gensalt()
#     # Hashing the password
#     hashed = bcrypt.hashpw(password_bytes, salt)
#     return hashed


jwt_bearer = jwtBearer()
# This function manages the hashing and verification of passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# This function takes a plain password and a hashed password,
# then uses pwd_context.verify() to verify whether the plain password matches the hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# This function takes a password as input and returns its hashed version
def get_password_hash(password):
    return pwd_context.hash(password)


# This function is checked if the provided username matches any stored username and if the provided password,
# once hashed and compared to the stored hashed password, matches the stored password
def check_user(our_user: UserLoginSchema):
    users = read_users()
    for stored_user in users:
        # Compare usernames and hashed passwords
        if stored_user["username"] == our_user.username and verify_password(our_user.password, stored_user["password"]):
            return True
    return False


# This function is a dependency used to check if the user is an admin. It takes a JWT token as input, verifies it using
# the verify_jwt method of jwt_bearer, and checks if the decoded token contains the role "admin"
def is_admin(token: str = Depends(jwt_bearer)):
    decoded_token = jwt_bearer.verify_jwt(token)
    if decoded_token.get("role") == "admin":
        return True
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to access this endpoint")
