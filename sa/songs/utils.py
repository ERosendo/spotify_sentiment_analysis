
from .services import SpotifyService
from dataclasses import dataclass

@dataclass
class Artist:
    uri: str
    name: str

@dataclass
class Album:
    uri: str
    name: str
    cover: str

@dataclass
class Song:
    name: str
    uri: str
    album: Album
    artist: list[Artist]
    

def search_song_by_name(name:str):
    if not name:
        return []
    
    sp_client = SpotifyService()
    data = sp_client.search(name, limit=12, type='track')
    song_list = []
    for song in data['tracks']['items']:
        artist = [Artist(x['uri'], x['name']) for x in song['artists']]
        album = Album(song['album']['uri'], song['album']['name'], song['album']['images'][0]['url'])
        song_data = Song(song['name'], song['uri'], album= album, artist=artist)
        song_list.append(song_data)
    
    return song_list