import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import Playlist, Review, Song
# from .forms import ReviewForm
from django.db.models import Q


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def reservations_index(request):
  reservations = Reservation.objects.filter(user=request.user)
  return render(request, 'reservations/index.html', {
    'reservations': reservations
  })

@login_required
def reservations_detail(request, reservation_id):
  reservation = Reservation.objects.get(id=reservation_id)
  id_list = reservation.songs.all().values_list('id')
#   songs_not_on_playlist = Song.objects.exclude(id__in=id_list)
  review_form = ReviewForm()
  return render(request, 'reservations/detail.html', {
    'reservation': reservation, 'review_form': review_form,
    # 'songs': songs_not_on_playlist
  })

# class PlaylistCreate(LoginRequiredMixin, CreateView):
#   model = Playlist
#   fields = ['title', 'purpose', 'description']

#   def form_valid(self, form):
#     form.instance.user = self.request.user
#     return super().form_valid(form)

# class PlaylistUpdate(UpdateView):
#   model = Playlist
#   fields = ['title', 'purpose', 'description']

# class PlaylistDelete(DeleteView):
#   model = Playlist
#   success_url = '/playlists'

# @login_required
# def add_review(request, playlist_id):
#   form = ReviewForm(request.POST)
#   if form.is_valid():
#     new_review = form.save(commit=False)
#     new_review.playlist_id = playlist_id
#     new_review.save()
#   return redirect('detail', playlist_id=playlist_id)  

# class SongList(LoginRequiredMixin, ListView):
#   model = Song

# class SongDetail(LoginRequiredMixin, DetailView):
#   model = Song

# class SongCreate(LoginRequiredMixin, CreateView):
#   model = Song
#   fields = '__all__'

# class SongUpdate(LoginRequiredMixin, UpdateView):
#   model = Song
#   fields = ['name', 'band', 'genre']

# class SongDelete(LoginRequiredMixin, DeleteView):
#   model = Song
#   success_url = '/songs'

# @login_required
# def assoc_song(request, playlist_id, song_id):
#   Playlist.objects.get(id=playlist_id).songs.add(song_id)
#   return redirect('detail', playlist_id=playlist_id)

# @login_required
# def unassoc_song(request, playlist_id, song_id):
#   Playlist.objects.get(id=playlist_id).songs.remove(song_id)
#   return redirect('detail', playlist_id=playlist_id)

# @login_required()
# def search_view(request):
#   query = request.GET.get('q', '')
#   results = Song.objects.filter(
#     Q(name__icontains=query) |
#     Q(band__icontains=query) |
#     Q(genre__icontains=query)
#   )
#   return render(request, 'search_results.html', {'results': results})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)