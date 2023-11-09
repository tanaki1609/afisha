from rest_framework import serializers
from films.models import Film, Director, Review, Genre
from rest_framework.exceptions import ValidationError


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name year age'.split()


# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    genres = serializers.SerializerMethodField()

    # all_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Film
        # fields = ['id', 'title', 'duration', 'rating_kinopoisk']
        fields = 'id title genres director rating reviews'.split()
        # exclude = ['id']
        depth = 1

    def get_genres(self, film):
        return [
            genre.title
            for genre in film.genres.all()
        ]


class FilmCreateValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=4, max_length=10)
    text = serializers.CharField(required=False)
    duration = serializers.IntegerField(default=0)
    rating = serializers.FloatField(min_value=1, max_value=10)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):  # 14
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return director_id

    def validate_genres(self, genres):  # [1,10,100]
        genres = list(set(genres))
        genre_db = Genre.objects.filter(id__in=genres)  # [1]
        if genre_db.count() != len(genres):
            raise ValidationError('Genre does not exist!')
        return genres

    def create_validated_data(self):
        validated = self.validated_data
        return {
            'title': validated['title'],
            'text': validated['text'],
            'rating_kinopoisk': validated['rating'],
            'duration': validated['duration'],
            'director_id': validated['director_id'],
        }


