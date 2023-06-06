import uuid
#from cassandra.cqlengine.models import Model
#from cassandra.cqlengine import columns
from sqlalchemy import Column, Text, UUID
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
    url = Column(Text)
    user_id = Column(UUID)

    def __str__(self):
        return self.__repr__()  

    def __repr__(self):
        return f"Video(host_id={self.host_id}, host_service={self.host_service})"
    
    
    @staticmethod
    def add_video(url, user_id=None):
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidYoutubeVideoURLException("Invalid Youtube Video URL")
        user_exists = User.check_exists(user_id)
        if user_exists is None:
            raise InvalidUserIDException("Invalid user_id")
        q = session.query(Video).allow_filtering().filter(Video.host_id==host_id, Video.user_id==user_id)
        if q.count() != 0:
            raise VideoAddedException("Video already added")
        return Video.create(host_id=host_id, user_id=user_id, url=url)
       