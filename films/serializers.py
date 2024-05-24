import datetime

from rest_framework import serializers
from .models import Film, Director, Tag, Review
from rest_framework.exceptions import ValidationError


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


class FilmValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=100)
    description = serializers.CharField(required=False)
    release_year = serializers.IntegerField(min_value=1897, max_value=datetime.datetime.now().year + 1)
    rating = serializers.FloatField(min_value=1, max_value=10)
    is_active = serializers.BooleanField()
    director_id = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    # def validate(self, attrs):
    #     print(attrs)
    #     try:
    #         Director.objects.get(id=attrs['director_id'])
    #     except:
    #         raise ValidationError('Director does not exist')
    #     return attrs

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except:
            raise ValidationError('Director does not exist')
        return director_id

    def validate_tags(self, tags):  # 1,2,3,1
        tags = list(set(tags))  # 1,2,3
        tags_from_db = [i.id for i in Tag.objects.filter(id__in=tags)]  # 1,2,3
        if len(tags_from_db) != len(tags):
            raise ValidationError('Tag does not exist')
        return tags
