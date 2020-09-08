from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('album/<int:album_id>/', views.album_details, name='detail')
]