from django.urls import path, include
from. import views

urlpatterns = [
  path('', views.home, name='home'),
  path('album/<int:album_id>/', views.album_details, name='detail'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup/', views.signup, name='signup'),
]