from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import include

from core.views import MovieViewSet, GenreViewSet, RatingViewSet, RentalCertificateViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('movies', MovieViewSet)
router.register('ratings', RatingViewSet)
router.register('genres', GenreViewSet)
router.register('rental_certificates', RentalCertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]