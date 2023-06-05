import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from application.config import get_settings
from application.users.models import User
from application.users.exceptions import InvalidUserIDException

settings = get_settings()

#from application.songs.extractors import extract_song_id
from application.songs.exceptions import InvalidSpotifySongURLException, SongAddedException

class Song(Model):
    __keyspace__ = settings.keyspace
    spotify_id = columns.Text(primary_key=True)
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    host_service = columns.Text(default='spotify')
    url = columns.Text()
    user_id = columns.UUID()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Song(host_id={self.host_id}, host_service={self.host_service})"
    
    '''
    @staticmethod
    def add_song(url, user_id=None):
        host_id = extract_song_id(url)
        if host_id is None:
            raise InvalidSpotifySongURLException("Invalid spotify song URL")
        user_exists = User.check_exists(user_id)
        if user_exists is None:
            raise InvalidUserIDException("Invalid user_id")
        q = Song.objects.allow_filtering().fliter(host_id=host_id, user_id=user_id)
        if q.count() != 0:
            raise SongAddedException("Song already added")
        return Song.create(host_id=host_id, user_id=user_id, url=url)
    '''    