from rest_framework import serializers
from .models import Film


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = 'id name is_active rating created_date'.split()


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = 'id name description release_year is_active rating created_date'.split()