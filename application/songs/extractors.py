#import requests
from urllib.parse import parse_qs, urlparse
from application.api import SpotifyAPI, client_id, client_secret

spotify1 = SpotifyAPI(client_id, client_secret)


def extract_artist_id(url):
    # Source: https://stackoverflow.com/a/54383711
    # Examples:
    # - https://api.spotify.com/v1/artists/0TnOYISbd1XYRBk9myase
    # - http://youtu.be/nNpvWBuTfrc
    # - http://www.youtube.com/watch?v=nNpvWBuTfrc&feature=feedu
    # - http://www.youtube.com/embed/nNpvWBuTfrc
    # - http://www.youtube.com/v/nNpvWBuTfrc?version=3&amp;hl=en_US
    query = urlparse(url)
    print(query.hostname)
    
    #if query.hostname == "api.spotify.com":
    #    return query.path[:4]
    #if query.hostname in {"www.youtube.com", "youtube.com"}:   
    if query.hostname in {"api.spotify.com", "spotify.com"}:
        #if query.path == "/watch":
        #if query.path == "/v1":
            #return parse_qs(query.query)["v"][0]
            #return parse_qs(query.query)["artists"]
        
        #if query.path == "/v1/":
        #    return query.path.split("/")[2]
    
        if query.path[:4] == "/v1/":
            return query.path.split("/")[3]
    '''    
        if query.path[:3] == "/v/":
            return query.path.split("/")[2]
        # # below is optional for playlists
        # if query.path[:9] == "/playlist":
        #     return parse_qs(query.query)["list"][0]
    return None
    '''
#print(extract_artist_id('https://api.spotify.com/v1/artists/0TnOYISbd1XYRBk9myase'))


def extract_user_id(url):
    query = urlparse(url)
    #print(query.hostname)

    if query.hostname in {"api.spotify.com", "spotify.com"}:
        if query.path[:4] == "/v1/":
            return query.path.split("/")[2]
        
print(extract_user_id('https://api.spotify.com/v1/me'))    



print(spotify1.search({"artist": "pitbull"}, search_type="track"))

