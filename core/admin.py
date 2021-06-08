from django.contrib import admin
from core.models import Movie, Rating, Genre, RentalCertificate

admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Genre)
admin.site.register(RentalCertificate)
