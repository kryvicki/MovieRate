from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from core.models import Movie, Rating, RentalCertificate, Genre
from core.serializers import MovieSerializer, \
    GenreSerializer, RentalCertificateSerializer, RatingSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    permission_classes_by_action = {'create': [AllowAny]}

    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def is_admin(self, request, pk=None):
        user = request.user
        response = {'is_admin': user.is_superuser}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating Updated',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating Created',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'You have to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    permission_classes_by_action = {'create': [IsAdminUser],
                                    'update': [IsAdminUser],
                                    'delete': [IsAdminUser]}

    def update(self, request, *args, pk=None):
        movie = Movie.objects.prefetch_related('genres').get(id=pk)
        movie.title = request.data['title']
        movie.description = request.data['description']
        movie.save()
        genres = GenreSerializer(request.data['genres'], many=True)
        movie.genres.clear()
        for genre in genres.data:
            genre_to_add = Genre.objects.get(pk=genre['id'])
            movie.genres.add(genre_to_add)
        movie.save()
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        title = request.data['title']
        description = request.data['description']
        genres = GenreSerializer(request.data['genres'], many=True)
        movie = Movie.objects.create(title=title, description=description)
        movie.genres.clear()
        for genre in genres.data:
            genre_to_add = Genre.objects.get(pk=genre['id'])
            movie.genres.add(genre_to_add)
        movie.save()
        return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You can not update rating this way'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You can not create rating this way'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RentalCertificateViewSet(viewsets.ModelViewSet):
    queryset = RentalCertificate.objects.all()
    serializer_class = RentalCertificateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=request.data['movie_id'])
        number = request.data['number']
        country = request.data['country']
        try:
            certifiacate = RentalCertificate.objects.create(number=number, country=country, movie=movie)
            serializer = RentalCertificateSerializer(certifiacate, many=False)
            response = {'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'result': 'same country and number set already exists, please choose another set'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
