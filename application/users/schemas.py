from pydantic import BaseModel, EmailStr, SecretStr, validator, root_validator
from application.users.models import User
from application.users import auth

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    session_id: str = None

    @root_validator
    def validate_user(cls, values):
        err_msg = "Inccorrect credentials, please try again."
        email = values.get('email')
        password = values.get('password')
        if email is None or password is None:
            raise ValueError(err_msg)
        password = password.get_secret_value()
        user_obj = auth.authenticate(email, password)
        if user_obj is None:
            raise ValueError(err_msg)
        token = auth.login(user_obj)
        return {"session_id": token} 

class UserSignupSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr
        
    @validator("email")
    def email_available(cls, v, values, **kwargs):
        q = User.objects.filter(email=v)
        if q.count() != 0:
            raise ValueError("Email is not Available")
        return v    
        
    @validator("confirm_password")
    def pass_match(cls, v, values, **kwargs):
        password = values.get("password")
        confirm_password = v
        if password != confirm_password:
            raise ValueError("password do not match")
        return v 