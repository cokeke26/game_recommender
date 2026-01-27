from django.db import models
from django.conf import settings

# Create your models here.

class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    platforms = models.ManyToManyField(Platform, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    cover_url = models.URLField(blank=True, default="")

    def __str__(self):
        return self.name
    
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "game")

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="liked_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "game")