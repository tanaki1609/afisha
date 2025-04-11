from rest_framework import serializers
from .models import Film, Director, Genre
from rest_framework.exceptions import ValidationError


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id fio age'.split()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(many=False)
    genres = GenreSerializer(many=True)
    director_fio = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = 'id reviews name kp_rating created director genres director_fio genre_names'.split()
        depth = 1

    def get_director_fio(self, film):
        return film.director.fio if film.director_id else None


class FilmValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=255)
    text = serializers.CharField(required=False, default='No text')
    kp_rating = serializers.FloatField(min_value=1, max_value=10)
    is_active = serializers.BooleanField(default=False)
    director_id = serializers.IntegerField(min_value=1)
    genres = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return director_id

    def validate_genres(self, genres):  # [1,2,3,10]
        genres_from_db = Genre.objects.filter(id__in=genres)  # [1,2,3]
        if len(genres_from_db) != len(genres):
            raise ValidationError('Genre does not exist!')
        return genres
