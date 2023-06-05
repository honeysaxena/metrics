from pydantic import BaseModel, validator, root_validator

class SongCreateSchema(BaseModel):
    url: str
    user_id: str