from django.shortcuts import render

from .utils import search_song_by_name, search_audio_features


def index(request):
    search_tex = request.GET.get('search')
    songs = search_song_by_name(search_tex)
    template = 'index.html'
    if request.htmx:
        template = 'search/partials/results.html'
    return render(request, template, context={ 'songs':songs})

def details(request, song_uri):
    template = 'details.html'
    song = search_audio_features(song_uri)
    return render(request, template, context={ 'song':song})