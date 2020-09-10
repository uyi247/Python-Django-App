from django.contrib import admin

# Register your models here.
from main_app.models import Collection, CollectionRating

admin.site.register(Collection)
admin.site.register(CollectionRating)