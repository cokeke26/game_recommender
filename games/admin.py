from django.contrib import admin
from .models import Game, Platform, Genre, Tag

admin.site.register(Game)
admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(Tag)
