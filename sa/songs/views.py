from utils import spotiscience
from django.shortcuts import render
from utils.spotiscience import CREDENTIALS

from .utils import search_audio_features, search_song_by_name

def index(request):
    search_tex = request.GET.get('search')
    songs = search_song_by_name(search_tex)
    template = 'index.html'
    if request.htmx:
        template = 'search/partials/results.html'
    return render(request, template, context={ 'songs':songs})

def details(request, song_uri):
    sp = spotiscience.SpotiSciencePredicter()
    sd = spotiscience.SpotiScienceDownloader(credentials=CREDENTIALS)
    template = 'details.html'
    song = search_audio_features(song_uri)
    song_to_analyze = sd.get_song_features(song_id=song_uri)
    mood = sp.predict_song_mood(song=song_to_analyze)
    return render(request, template, context={ 'song':song, 'mood': mood})