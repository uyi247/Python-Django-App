from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import requests
import json
from django.urls import reverse
from main_app.models import Album, Collection, CollectionRating
from main_app.forms import RatingForm, RatingUserForm
from django.contrib.auth.models import User

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
    song_response = requests.get('https://theaudiodb.com/api/v1/json/1/track.php?m='+ str(album_id))
    songs = song_response.json()
    song_list =[]
    i = 0
    while i < len(songs['track']):
      song_list.append(str(i+1) + '. ' + songs['track'][i]['strTrack'])
      i+=1
    album = response.json()
    return render(request, 'album_detail.html', {
      'album_name': album['album'][0]['strAlbum'],
      'album_art': album['album'][0]['strAlbumThumb'],
      'album_back': album['album'][0]['strAlbumThumbBack'],
      'artist_name': album['album'][0]['strArtist'],
      'genre': album['album'][0]['strGenre'],
      'sales': album['album'][0]['intSales'],
      'album_description': album['album'][0]['strDescriptionEN'],
      'pk': album_id,
      'collection': Collection.objects.filter(user=request.user, album=album_id).first(),
      'song_list': song_list,
    })

@login_required
def add_to_collection(request, album_id):  
  response = requests.get('https://theaudiodb.com/api/v1/json/1/album.php?m='+ str(album_id))
  album = response.json()
  collection, _ = Collection.objects.get_or_create(album=album_id, user=request.user)
  collection.title = album['album'][0]['strAlbum']
  collection.art_url = album['album'][0]['strAlbum3DCase']
  collection.artist = album['album'][0]['strArtist']
  collection.save()
  return redirect(reverse('detail', kwargs={'album_id': album_id}))

@login_required
def remove_from_collection(request, album_id):  
  collection, _ = Collection.objects.get_or_create(album=album_id, user=request.user)
  collection.delete()
  return redirect(reverse('detail', kwargs={'album_id': album_id}))

@login_required
def rate_collection(request, album_id, user_id=None):  
  if  user_id:
    
    collection, _ = CollectionRating.objects.get_or_create(album=album_id, user_collection_id=user_id, user_rating=request.user)
    form = RatingUserForm(request.POST or None, instance=collection)
  else:
    try:
      collection, _ = Collection.objects.get_or_create(album=album_id, user=request.user)
    except:
      collection = Collection.objects.filter(album=album_id, user=request.user).first()
      pass
    form = RatingForm(request.POST or None, instance=collection)
  if request.method == "POST":
    if form.is_valid():
      collection = form.save(False)
      collection.user = request.user
      collection.save()
      if user_id:
        return redirect(reverse('collection', kwargs={'user_id': user_id}))
      return redirect(reverse('detail', kwargs={'album_id': album_id}))
  return render(request, 'rate.html', {'form': form})
  #collection, _ = Collection.objects.get_or_create(album=album_id, user=request.user)
  #return redirect(reverse('detail', kwargs={'album_id': album_id}))

@login_required
def collection( request):
  collections = Collection.objects.filter(user=request.user)
  for collection in collections:
    collection.user_ratings = CollectionRating.objects.filter(album=collection.album, user_collection_id=request.user)
  return render(request, 'collection.html', {'collections': collections})


def collections(request):
  users = User.objects.all().prefetch_related('collection_set')
  for user in users:
    user_collection =  CollectionRating.objects.filter(user_rating=request.user, user_collection=user).first()
    
    user.rating = user_collection
  context = {
    'users': users,
    'stars': range(5)
  }
  return render(request, 'collections.html', context)

def user_collection(request, user_id):
  collections = Collection.objects.filter(user_id=user_id)
  for collection in collections:
    collection.user_ratings = CollectionRating.objects.filter(
      user_rating=request.user, album=collection.album, user_collection_id=user_id)
    print(collection.user_ratings)
  return render(request, 'collection.html', {'collections': collections, 'user_id': user_id})

def rate_user_collection(request, user_id, stars):
  rating, _ = CollectionRating.objects.get_or_create(user_rating=request.user, user_collection_id=user_id)
  rating.rating = stars
  rating.save()
  return HttpResponse(json.dumps({'msg': 'ok'}))

def review_collection(request, user_id):
  rating, _ = CollectionRating.objects.get_or_create(user_rating=request.user, user_collection_id=user_id)
  rating.review = request.POST.get('review')
  rating.save()
  return redirect('collections')