from django.db import models

# Create your models here.
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User

class albums(models.Model):
  name = models.CharField(max_length=50)
  artist = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('albums_detail', kwargs={'pk': self.id})

    class Collection(models.Model):
      name = models.CharField(max_length=100)
      songs = models.CharField(max_length=100)
      description = models.TextField(max_length=250)
      albums = models.ManyToManyField(album)
      user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('detail', kwargs={'collection_id': self.id})