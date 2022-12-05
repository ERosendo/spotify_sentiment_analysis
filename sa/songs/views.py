from utils import spotiscience
from django.shortcuts import render
from django.http import HttpResponse
from utils.spotiscience import CREDENTIALS

from .utils import search_audio_features, search_song_by_name

def index(request):
    search_text = request.GET.get('search')
    songs = search_song_by_name(search_text)
    template = 'index.html'
    if request.htmx:
        template = 'search/partials/results.html'
    return render(request, template, context={ 'songs':songs})

def details(request, song_uri):
    template = 'details.html'
    song = search_audio_features(song_uri)
    return render(request, template, context={ 'song':song })


def moods(request, song_uri):
    sp = spotiscience.SpotiSciencePredicter()
    sd = spotiscience.SpotiScienceDownloader(credentials=CREDENTIALS)
    song_to_analyze = sd.get_song_features(song_id=song_uri)
    mood = sp.predict_song_mood(song=song_to_analyze)
    return HttpResponse(f'{mood}')