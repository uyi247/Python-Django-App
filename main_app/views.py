from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
import requests

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def home(request):
  return render(request, 'home.html')

def signup(request):
  error_message = ''
  form = UserCreationForm(request.POST or None)
  if request.method == 'POST':    
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'

  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def home(request):
    responsetop50 = requests.get('https://theaudiodb.com/api/v1/json/523532/mostloved.php?format=album')
    top50 = responsetop50.json()
    album_id = []
    album_art_top50 = []
    i = 0
    while i < len(top50['loved']):
        album_id.append(top50['loved'][i]['idAlbum'])
        album_art_top50.append(top50['loved'][i]['strAlbumThumb'])
        i+=1
    zipped_list = zip(album_id, album_art_top50)
    return render(request, 'home.html', {
      'id_and_art': zipped_list,
      'album_id' : album_id,
      'album_art_top50': album_art_top50,
    })

def album_details(request, album_id):
    response = requests.get('https://theaudiodb.com/api/v1/json/1/album.php?m='+ str(album_id))
    album = response.json()
    return render(request, 'album_detail.html', {
      'album_name': album['album'][0]['strAlbum'],
      'album_art': album['album'][0]['strAlbumThumb'],
      'album_back': album['album'][0]['strAlbumThumbBack'],
      'artist_name': album['album'][0]['strArtist'],
      'genre': album['album'][0]['strGenre'],
      'sales': album['album'][0]['intSales'],
      'album_description': album['album'][0]['strDescriptionEN'],
    })
