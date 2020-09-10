from django.db import models

# Create your models here.
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User

class Album(models.Model):
  name = models.CharField(max_length=100)
  artist = models.CharField(max_length=100)
  genre = models.CharField(max_length=100)
  description = models.TextField(default='')
  art = models.URLField(default='')

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('albums_detail', kwargs={'pk': self.id})


class Collection(models.Model):
  RATING_CHOICES = [[x,x] for x in range(1 ,6)]
  album = models.IntegerField(Album, default=0)
  title = models.CharField(max_length=100, default="")
  art_url = models.URLField(max_length=255, default="")
  artist = models.CharField(max_length=100, default='NA')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  rating = models.IntegerField(choices=RATING_CHOICES,blank=True, null=True, default=5)
  review = models.TextField(blank=True, null=True)


class CollectionRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_rated')
    album = models.IntegerField(Album, default=0)
    title = models.CharField(max_length=100, default="")
    art_url = models.URLField(max_length=255, default="")
    artist = models.CharField(max_length=100, default='NA')
    rating = models.IntegerField(default=5)
    review = models.TextField(blank=True, null=True)