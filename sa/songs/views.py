import io

from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from utils import spotiscience
from utils.spotiscience import CREDENTIALS

from .models import Album, Artist, AudioFeature, Song
from .utils import search_audio_features, search_song_by_name, get_song_from_db


def index(request):
    search_text = request.GET.get('search')
    songs = search_song_by_name(search_text)
    template = 'index.html'
    if request.htmx:
        template = 'search/partials/results.html'
    return render(request, template, context={'songs': songs})


def details(request, song_uri):
    template = 'details.html'
    db_song = Song.objects.filter(uri=song_uri).first()
    if db_song:
        song = get_song_from_db(db_song)
    else:
        song = search_audio_features(song_uri)
        db_album = Album.objects.filter(uri=song['data'].album.uri).first()
        if db_album:
            album = db_album
        else:
            album = Album.objects.create(
                name=song['data'].album.name,
                cover=song['data'].album.cover,
                uri=song['data'].album.uri)
        
        for artist_data in song['data'].artist:
            db_artist = Artist.objects.filter(uri=artist_data.uri).first()
            if db_artist:
                if not album.artist.filter(id = db_artist.id).exists():
                    album.artist.add(db_artist)
            else:
                artist = Artist.objects.create(
                    name=artist_data.name,
                    uri=artist_data.uri
                )
                album.artist.add(artist)

        new_song = Song.objects.create(
            album=album,
            name=song['data'].name,
            uri=song['data'].uri
        )

        AudioFeature.objects.create(
            song=new_song,
            acousticness = song['audio_features']['acousticness'],
            danceability = song['audio_features']['danceability'],
            energy = song['audio_features']['energy'],
            instrumentalness = song['audio_features']['instrumentalness'],
            liveness = song['audio_features']['liveness'],
            speechiness = song['audio_features']['speechiness'],
            loudness = song['audio_features']['loudness'],
            valence = song['audio_features']['valence'],
            tempo = song['audio_features']['tempo'],
        ) 
    return render(request, template, context={'song': song})


def moods(request, song_uri):
    db_song = Song.objects.filter(uri=song_uri).first()
    if db_song.mood:
        mood = db_song.mood
    else:
        sp = spotiscience.SpotiSciencePredicter()
        sd = spotiscience.SpotiScienceDownloader(credentials=CREDENTIALS)
        song_to_analyze = sd.get_song_features(song_id=song_uri)
        mood = sp.predict_song_mood(song=song_to_analyze)
        db_song.mood = mood
        db_song.save()
    template = 'mood/index.html'
    return render(request, template, context={'mood': mood.capitalize(), 'song_uri': song_uri})


def some_view(request, song_uri):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    db_song = Song.objects.filter(uri=song_uri).first()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, db_song.name)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'{db_song.name}.pdf')
