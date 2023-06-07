import uuid
from pydantic import BaseModel, validator, root_validator
from application.videos.extractors import extract_video_id
from application.videos.exceptions import InvalidYoutubeVideoURLException, VideoAddedException
from application.users.exceptions import InvalidUserIDException
from application.videos.models import Video
from application.videos.models import session
#from application.db import SessionLocal


#session = SessionLocal()

class VideoCreateSchema(BaseModel):
    url: str
    title: str
    user_id: uuid.UUID

    @validator("url")
    def validate_youtube_url(cls, v, values, **kwargs):
        url = v
        video_id = extract_video_id(v)
        if video_id is None:
            raise ValueError(f'{url} is not a valid youtube URL')
        return url
    
    @root_validator
    def validate_data(cls, values):
        url = values.get('url')
        title = values.get('title') 
        if url is None:
            raise ValueError("A valid URL is required.")
        user_id = values.get('user_id')
        video_obj = None
        extra_data = {}
        if title is not None:
            extra_data["title"] = title
        try:
            video_obj = Video.add_video(url, user_id=user_id, **extra_data)
        except InvalidYoutubeVideoURLException:
            raise ValueError(f"{url} is not a valid youtube URL")
        except VideoAddedException:
            raise ValueError(f"{url} is already been added.")
        except InvalidUserIDException:
            raise ValueError("There is a problem with your account, please try again")
        except:
            raise ValueError("There is a problem with your account, please try again")
        if video_obj is None:
           raise ValueError("There is a problem with your account, please try again")
        if not isinstance(video_obj, Video):
            raise ValueError("There is a problem with your account, please try again")
        #if title is not None:
        #    video_obj.title = title
        #    session.add(video_obj)
        #    session.commit()
        #    session.refresh(video_obj)
        return video_obj.as_data() 
