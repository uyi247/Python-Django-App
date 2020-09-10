from django.urls import path, include
from. import views

urlpatterns = [
  path('', views.home, name='home'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup/', views.signup, name='signup'),
  path('album/<int:album_id>/', views.album_details, name='detail'),
  path('collection', views.collection, name='collection'),
  path('collections', views.collections, name='collections'),
  path('collections/<int:user_id>', views.user_collection, name='collection'),
  path('collections/<int:user_id>/<int:stars>/', views.rate_collection, name='rate_collection'),
  #path('collections/<int:user_id>/', views.review_collection, name='review_collection'),
  path('album/<int:album_id>/add-collection', views.add_to_collection, name='add_to_collection'),
  path('album/<int:album_id>/remove-collection', views.remove_from_collection, name='remove_from_collection'),
  path('album/<int:album_id>/remove-rating', views.remove_rating, name='remove_rating'),
  path('album/<int:album_id>/rate-collection/', views.rate_collection, name='rate_collection'),
  path('album/<int:album_id>/rate-collection/<int:user_id>/', views.rate_collection, name='rate_collection'),
]