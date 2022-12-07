from core.models import BaseModel
from django.db import models


class Artist(BaseModel):
    uri = models.CharField(max_length=256)
    name = models.CharField(max_length=256)


class Album(BaseModel):
    artist = models.ManyToManyField(Artist)
    uri = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    cover = models.CharField(max_length=256)


class Song(BaseModel):
    album = models.ForeignKey(
        Album,
        related_name='songs',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    uri = models.CharField(max_length=256)
    mood = models.CharField(max_length=256, null=True)
    
class AudioFeature(BaseModel):
    song = models.OneToOneField(Song, related_name='audio_features', on_delete=models.CASCADE)
    acousticness = models.FloatField(null=True, blank=True, default=None)
    danceability = models.FloatField(null=True, blank=True, default=None)
    energy = models.FloatField(null=True, blank=True, default=None)
    instrumentalness = models.FloatField(null=True, blank=True, default=None)
    liveness = models.FloatField(null=True, blank=True, default=None)
    speechiness = models.FloatField(null=True, blank=True, default=None)
    loudness = models.FloatField(null=True, blank=True, default=None)
    valence = models.FloatField(null=True, blank=True, default=None)
    tempo = models.FloatField(null=True, blank=True, default=None)