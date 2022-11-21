from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:song_uri>', views.details, name='detail'),
]