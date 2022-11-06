from django.shortcuts import render

from .utils import search_song_by_name


def index(request):
    search_tex = request.GET.get('search')
    print(search_tex)
    songs = search_song_by_name(search_tex)
    template = 'index.html'
    if request.htmx:
        template = 'search/partials/results.html'
    return render(request, template, context={ 'songs':songs})