from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmSerializer, FilmDetailSerializer


@api_view(['GET'])
def films_list_api_view(request):
    # step 1: Collect data from DB
    films = Film.objects.all()

    # step 2: List of films from DB convert to Dictionary
    list_ = FilmSerializer(films, many=True).data

    # step 3: Return list of dictionary as JSON
    return Response(data=list_, status=status.HTTP_200_OK)


@api_view(['GET'])
def films_detail_api_view(request, id): # 100
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Film not found'})
    film_dict = FilmDetailSerializer(film).data
    return Response(data=film_dict)
