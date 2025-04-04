from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmSerializer, FilmDetailSerializer


@api_view(['GET'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = FilmDetailSerializer(film).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def film_list_api_view(request):
    # step 1: Collect data from DB (QuerySet)
    films = (Film.objects.select_related('director')
             .prefetch_related('genres', 'reviews').all())

    # step 2: Reformat (Serialize) QuerySet to List of dict
    data = FilmSerializer(films, many=True).data

    # step 3: Return Response
    return Response(data=data,
                    status=status.HTTP_200_OK)  # data=(list, dict), status=int
