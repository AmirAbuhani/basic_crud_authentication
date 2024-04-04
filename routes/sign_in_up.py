from fastapi import APIRouter, HTTPException, Body, Depends
from models.users_model import UserSchema, UserLoginSchema
from read_write_users_db import read_users, write_users
from utils.auth_fns import check_user, get_password_hash
from auth.jwt_handler import signJWT
from auth.jwt_bearer import jwtBearer

router = APIRouter()

jwt_bearer = jwtBearer()


# This route is used for user sign-up. It expects a UserSchema object in the request body. It hashes the password,
# writes the user data to the database, signs a JWT token using the signJWT function, and returns it
@router.post("/user/sign-up", tags=["authentication"])
def sign_up(user: UserSchema = Body(default=None)):
    try:
        password = get_password_hash(user.password)
        write_users(user.username, password)
        role = user.role
        return signJWT(user.username, role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# This route is used for user sign-in. It expects a UserLoginSchema object in the request body.
# It checks if the user exists and if the provided password is correct using the check_user function
@router.post("/user/sign-in", tags=["authentication"])
def sign_in(user: UserLoginSchema = Body(default=None)):
    try:
        user_role = user.role

        # Check if the user exists and the password is correct
        if check_user(user):
            # If the user exists and password is correct, return JWT token
            return signJWT(user.username, user_role)
        else:
            # If user authentication fails, return error message
            return {
                "error": "Invalid login details!"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# This function is a dependency used to check if the user is an admin. It takes a JWT token as input, verifies it using
# the verify_jwt method of jwt_bearer, and checks if the decoded token contains the role "admin"
def is_admin(token: str = Depends(jwt_bearer)):
    decoded_token = jwt_bearer.verify_jwt(token)
    if decoded_token.get("role") == "admin":
        return True
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to access this endpoint")
