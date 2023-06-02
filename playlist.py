from urllib.parse import urlencode
import api
import requests
from fastapi import Header, Depends
from typing import Annotated
from fastapi.responses import RedirectResponse


headers = {"Authorization": f"Bearer {api.spotify.access_token}"}
endpoint = "https://api.spotify.com/v1/search"
data = urlencode({"q": "Time", "type": "track"})
print(data)

lookup_url = f"{endpoint}?{data}"
print(lookup_url)

r = requests.get(lookup_url, headers=headers)
print(r.status_code)
# print(r.json())
