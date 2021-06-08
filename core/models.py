from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    class Meta:
        default_related_name = 'genres'


class Movie(models.Model):
    title = models.CharField(max_length=50, db_index=True)
    description = models.TextField(max_length=500, db_index=True)
    genres = models.ManyToManyField(Genre, blank=True)

    class Meta:
        default_related_name = 'movies'

    def ratings_amount(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def average_rating(self):
        sum = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            sum += rating.stars
        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0


class RentalCertificate(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, primary_key=True)
    number = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        unique_together = ['number', 'country']
        index_together = ['number', 'country']


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], db_index=True)

    class Meta:
        unique_together = ['user', 'movie']
        index_together = ['user', 'movie']


