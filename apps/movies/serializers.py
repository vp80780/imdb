from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Movies, Genre


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MoviesSerializer(ModelSerializer):
    genre = GenreSerializer(required=False, many=True)
    class Meta:
        model = Movies
        fields = '__all__'


class MoviesCreateSerializer(ModelSerializer):
    genre = serializers.ListField(write_only=True)

    class Meta:
        model = Movies
        fields = '__all__'

    def create(self, validated_data):
        genre_data = validated_data.pop('genre')
        movie = Movies.objects.create(**validated_data)
        for genre in genre_data:
            genre, created = Genre.objects.get_or_create(genre=genre)
            movie.genre.add(genre)
        return movie
