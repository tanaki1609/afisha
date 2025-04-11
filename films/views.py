from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film, Director
from .serializers import FilmSerializer, FilmDetailSerializer, FilmValidateSerializer
from django.db import transaction


@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = FilmDetailSerializer(film).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = FilmValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        film.name = serializer.validated_data.get('name')
        film.text = serializer.validated_data.get('text')
        film.kp_rating = serializer.validated_data.get('kp_rating')
        film.is_active = serializer.validated_data.get('is_active')
        film.director_id = serializer.validated_data.get('director_id')
        film.genres.set(serializer.validated_data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def film_list_create_api_view(request):
    if request.method == 'GET':
        # step 1: Collect data from DB (QuerySet)
        films = (Film.objects.select_related('director')
                 .prefetch_related('genres', 'reviews').all())

        # step 2: Reformat (Serialize) QuerySet to List of dict
        data = FilmSerializer(films, many=True).data

        # step 3: Return Response
        return Response(data=data,
                        status=status.HTTP_200_OK)  # data=(list, dict), status=int
    elif request.method == 'POST':
        # step 0: Validation (Existing, Typing, Extra)
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # step 1: Receive data from Serialized data
        name = serializer.validated_data.get('name')
        text = serializer.validated_data.get('text')
        kp_rating = serializer.validated_data.get('kp_rating')
        is_active = serializer.validated_data.get('is_active')  # "Y"
        director_id = serializer.validated_data.get('director_id')  # 10
        genres = serializer.validated_data.get('genres')

        # step 2: Create film by received data
        with transaction.atomic():
            film = Film.objects.create(
                name=name,
                text=text,
                kp_rating=kp_rating,
                is_active=is_active,
                director_id=director_id,
            )
            film.genres.set(genres)
            film.save()

        # step 3: Return Response (status=201, data=CreatedFilm)
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
