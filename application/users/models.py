import uuid
#from cassandra.cqlengine.models import Model
#from cassandra.cqlengine import columns
from sqlalchemy import Column, Text, UUID, String
from application.config import get_settings
from application.users import validators, security, exceptions
from application.config import get_settings
from application.db import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from fastapi import Depends

settings = get_settings()

session = SessionLocal()

class User(Base):
    __tablename__ = 'users'
    email = Column(Text, primary_key=True)
    user_id = Column(UUID, primary_key=True, default=uuid.uuid1)
    password = Column(Text)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email}, user_id={self.user_id})"
    
    def set_password(self, pw, commit=False):
        pw_hash = security.generate_hash(pw)
        self.password = pw_hash
        if commit:
            self.save()
        return True 

    def verify_password(self, pw_str):
        pw_hash = self.password
        verified, _ = security.verify_hash(pw_hash, pw_str)
        return verified   
    
    #@staticmethod
    #def create_user(email, password=None):
    #    q = User.objects.filter(email=email)
    #    if q.count() != 0:
    #        raise exceptions.UserHasAccountException("user already has account with this email")
    #    valid, msg, email = validators._validate_email(email)
    #    if not valid:
    #        raise exceptions.InvalidEmailException(f"Invalid email: {msg}")
    #    obj = User(email=email)
    #    obj.set_password(password)
    #    #obj.password = password
    #    obj.save()
    #     return obj

    @staticmethod
    def create_user(email: Text, password: Text = None):
        q = session.query(User).filter(User.email==email)
        print(q)
        if q.count() != 0:
            raise exceptions.UserHasAccountException("user already has account with this email")
        valid, msg, email = validators._validate_email(email)
        if not valid:
            raise exceptions.InvalidEmailException(f"Invalid email: {msg}")
        obj = User(email=email)
        obj.set_password(password)
        #obj.password = password
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj 
    
    @staticmethod
    def check_exists(user_id):
        q = session.query(User).filter(User.user_id==user_id)
        return q.count() != 0
    
    @staticmethod
    def by_user_id(user_id=None):
        if user_id is None:
            return None
        q = session.query(User).filter(User.user_id==user_id)
        if q.count() != 1:
            return None
        return q.first()
    

Base.metadata.create_all(bind=engine)

#user1 = User.create_user(email='admin@gmail.com', password='abc123')
#print(user1) 
#obj = User.by_user_id(user_id='8ccf1e1e-0494-11ee-a3c9-c87dd83ba6d7')
#print(obj)

