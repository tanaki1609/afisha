from rest_framework import serializers
from .models import Film, Director, Tag, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text stars'.split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'fio age'.split()


class FilmSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    tags = TagSerializer(many=True)
    filtered_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = 'id filtered_reviews director director_fio tag_names tags name is_active rating created_date'.split()
        # depth = 1

    def get_filtered_reviews(self, film):
        reviews = [i for i in film.reviews.all() if i.stars > 6]
        return ReviewSerializer(reviews, many=True).data


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = 'id name description release_year is_active rating created_date'.split()
