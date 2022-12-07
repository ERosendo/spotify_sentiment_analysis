
from dataclasses import asdict, dataclass

from .services import SpotifyService


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


AUDIO_FEATURES_FOR_POLAR_GRAPH = ['acousticness',
                                'danceability',
                                'energy',
                                'instrumentalness',
                                'liveness',
                                'speechiness',
                                'valence']

def extract_song_data(track) -> Song:
    artist = [Artist(x['uri'], x['name']) for x in track['artists']]
    album = Album(track['album']['uri'], track['album']
                  ['name'], track['album']['images'][0]['url'])
    uri = track['uri'].split(':')[-1]
    return Song(track['name'], uri, album=album, artist=artist)

def extract_audio_features(raw_features):
    labels = []
    data = []
    if isinstance(raw_features, dict):
        feature = raw_features
    else:
        feature = raw_features.__dict__
    for k, v in feature.items():
        if k in AUDIO_FEATURES_FOR_POLAR_GRAPH:
            labels.append(k)
            data.append(v)
    return labels, data

def search_song_by_name(name: str):
    if not name:
        return []

    sp_client = SpotifyService()
    data = sp_client.search(name, limit=12, type='track')
    song_list = []
    for song in data['tracks']['items']:
        song_data = extract_song_data(song)
        song_list.append(song_data)

    return song_list


def search_audio_features(uri: str):
    sp_client = SpotifyService()

    raw_audio_features = sp_client.get_audio_features(f'spotify:track:{uri}')
    raw_song_data = sp_client.get_song_data(f'spotify:track:{uri}')
    song_data = extract_song_data(raw_song_data)
    label , values = extract_audio_features(raw_audio_features)

    return {'data': song_data, 'audio_features': raw_audio_features, 'labels': label, 'feature_value': values}


def get_song_from_db(db_song):
    label, values = extract_audio_features(db_song.audio_features)
    song_data = { 'name': db_song.name, 'uri': db_song.uri, 'album': db_song.album , 'artist':db_song.album.artist }
    return {'data': song_data, 'audio_features': db_song.audio_features, 'labels': label, 'feature_value': values}