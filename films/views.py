from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film, Director
from .serializers import FilmSerializer, FilmDetailSerializer


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
        film.name = request.data.get('name')
        film.text = request.data.get('text')
        film.kp_rating = request.data.get('kp_rating')
        film.is_active = request.data.get('is_active')
        film.director_id = request.data.get('director_id')
        film.genres.set(request.data.get('genres'))
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
        # step 1: Receive data from RequestBody
        name = request.data.get('name')
        text = request.data.get('text')
        kp_rating = request.data.get('kp_rating')
        is_active = request.data.get('is_active')
        director_id = request.data.get('director_id')  # 1
        genres = request.data.get('genres')

        # step 2: Create film by received data
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
