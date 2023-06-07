from application.users.models import User
import datetime
from jose import jwt
from application import config
from application.db import engine, SessionLocal, Base


settings = config.get_settings()
session = SessionLocal()

def authenticate(email, password):
    #user_obj = session.query(User).filter_by(email=email).all()
    #for i in user_obj:
    #    print(i.email)

    
    try:
        user_obj = session.query(User).filter_by(email=email).all()    
    except Exception as e:
        user_obj = None 
    for user in user_obj:       
        if not user.verify_password(password):
            return None
    return user
    

def login(user_obj, expires=settings.session_duration):  
    raw_data = {
    "user_id": f"{user_obj.user_id}",
    "role": "admin",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires)    
    }
    return jwt.encode(raw_data, settings.secret_key, algorithm=settings.jwt_algorithm)

def verify_user_id(token):
    data = {}
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError as e:
        print(e, "log out user")
    except:
        pass
    if "user_id" not in data:
        return None
    return data

#print(authenticate('test@gmail.com', 'abc123'))