from pydantic import BaseModel, validator, root_validator
from application.videos.extractors import extract_artist_id

class PlaylistCreateSchema(BaseModel):
    url: str
    user_id: str

    @validator("url")
    def validate_spotify_url(cls, v, values, **kwargs):
        url = v
