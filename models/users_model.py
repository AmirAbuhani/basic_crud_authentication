from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    email: EmailStr = Field(default=None)
    username: str = Field(default=None)
    password: str = Field(default=None)
    role: str = Field(default="admin")


class UserLoginSchema(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    role: str = Field(default="admin")
