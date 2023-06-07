import uuid
#from cassandra.cqlengine.models import Model
#from cassandra.cqlengine import columns
from sqlalchemy import Column, Text, UUID, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from application.config import get_settings
from application.users.models import User
from application.users.exceptions import InvalidUserIDException
from application.db import Base, engine, SessionLocal

settings = get_settings()

session = SessionLocal()
Base.metadata.create_all(bind=engine)


from application.videos.extractors import extract_video_id
from application.videos.exceptions import InvalidYoutubeVideoURLException, VideoAddedException

class Video(Base):
    __tablename__ = 'videos'
    host_id = Column(Text, primary_key=True)
    db_id = Column(UUID, primary_key=True, default=uuid.uuid1)
    host_service = Column(Text, default='youtube')
    title = Column(Text)
    url = Column(Text)
    user_id = Column(UUID)
    #user_id = Column(ForeignKey('users.user_id'))
    #users = relationship("User")
    #user_id = relationship("User", foreign_keys="Video.user_id")  


    def __str__(self):
        return self.__repr__()  

    def __repr__(self):
        return f"Video(title={self.title}, host_id={self.host_id}, host_service={self.host_service})"
    
    def as_data(self):
        return {f"{self.host_service}_id": self.host_id, "path": self.path}
    
    @property
    def path(self):
        return f"/videos/{self.host_id}"   
    
    
    @staticmethod
    def add_video(url, user_id=None, **kwargs):
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidYoutubeVideoURLException("Invalid Youtube Video URL")
        user_exists = User.check_exists(user_id)
        if user_exists is None:
            raise InvalidUserIDException("Invalid user_id")
        
        q = session.query(Video).filter(Video.host_id==host_id, Video.user_id==user_id, Video.url==url)
        if q.count() != 0:
            raise VideoAddedException("Video added")
        
        #obj = Video(host_id=host_id, url=url, user_id=user_id)
        obj = Video(host_id=host_id, user_id=user_id, url=url, **kwargs)
        session.add(obj)
        
        session.commit()
        session.refresh(obj)
        return obj
    

#obj = Video.add_video('https://www.youtube.com/watch?v=gAcuTqZGvmg&ab_channel=GypsyinSneakers', user_id='8ccf1e1e-0494-11ee-a3c9-c87dd83ba6d7')
#print(obj)