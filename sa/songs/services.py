import spotipy
from sa.settings import SPOTIFY_CID, SPOTIFY_SECRET
from spotipy.oauth2 import SpotifyClientCredentials



class SpotifyService():
    
    def __init__(self) -> None:
        self.client = spotipy.Spotify(
            client_credentials_manager = SpotifyClientCredentials(
                client_id=SPOTIFY_CID, 
                client_secret=SPOTIFY_SECRET
                )
            )
        
    def search(self, name:str, limit:int, type:str):
        return self.client.search(name, limit=limit, type=type)