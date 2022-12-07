from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:song_uri>', views.details, name='detail'),
    path('<slug:song_uri>/mood/', views.moods, name='mood_for_song'),
    path('<slug:song_uri>/pdf/', views.some_view, name='pdf_report')
]
