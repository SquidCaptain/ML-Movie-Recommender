from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    movieId = models.IntegerField(unique=True)
    tmdbId = models.IntegerField(null=True, blank=True)

    title = models.CharField(max_length=255)
    genres = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    directors = models.TextField(blank=True)
    actors = models.TextField(blank=True)

    poster_path = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.movie} ({self.rating})"