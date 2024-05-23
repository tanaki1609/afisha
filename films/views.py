from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmSerializer, FilmDetailSerializer


@api_view(['GET', 'POST'])
def films_list_api_view(request):
    if request.method == 'GET':
        # step 1: Collect data from DB
        films = Film.objects.select_related('director').prefetch_related('tags', 'reviews').all()

        # step 2: List of films from DB convert to Dictionary
        list_ = FilmSerializer(films, many=True).data

        # step 3: Return list of dictionary as JSON
        return Response(data=list_, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # step 1: Get data from RequestBody
        name = request.data.get('name')
        text = request.data.get('description')
        release_year = request.data.get('release_year')
        rating = request.data.get('rating')
        is_active = request.data.get('is_active')
        director_id = request.data.get('director_id')
        tags = request.data.get('tags')

        # step 2: Create Film by received data
        film = Film.objects.create(
            name=name,
            description=text,
            release_year=release_year,
            rating=rating,
            is_active=is_active,
            director_id=director_id,
        )
        film.tags.set(tags)
        film.save()

        # step 3: Return right status and created data
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)


@api_view(['GET', 'PUT', 'DELETE'])
def films_detail_api_view(request, id):  # 100
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Film not found'})
    if request.method == 'GET':
        film_dict = FilmDetailSerializer(film).data
        return Response(data=film_dict)
    elif request.method == 'PUT':
        film.name = request.data.get('name')
        film.description = request.data.get('description')
        film.is_active = request.data.get('is_active')
        film.rating = request.data.get('rating')
        film.release_year = request.data.get('release_year')
        film.director_id = request.data.get('director_id')
        film.tags.set(request.data.get('tags'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
    elif request.method == 'DELETE':
        try:
            film.delete()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': 'Film protected'})
        return Response(status=status.HTTP_204_NO_CONTENT)
