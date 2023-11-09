from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from films.models import Film, Director, Genre
from films.serializers import FilmSerializer, \
    FilmCreateValidateSerializer, DirectorSerializer, GenreSerializer
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class FilmListCreateAPIView(ListCreateAPIView):
    serializer_class = FilmSerializer
    queryset = Film.objects.all()
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            # Step 0. Validation
            serializer = FilmCreateValidateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'message': 'Request failed',
                                      'errors': serializer.errors})

            # Step 1. Get data from validated data
            genres = serializer.validated_data.get('genres')

            # Step 2. Create Film with data
            film = Film.objects.create(**serializer.create_validated_data())
            film.genres.set(genres)
            film.save()

            # Step 3. Return response (status) as created object
            return Response(status=status.HTTP_201_CREATED,
                            data={'message': "Film created",
                                  'film': {'id': film.id, 'title': film.title}})


class GenreAPIViewSet(ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class DirectorListCreateAPIView(ListCreateAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    pagination_class = PageNumberPagination


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    lookup_field = 'id'


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def film_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # Step 1. colllect data
        films = Film.objects.select_related('director') \
            .prefetch_related('genres', 'reviews').all()

        # Step 2. convert data to dict
        films_json = FilmSerializer(instance=films, many=True).data

        # Step 3. return dict as json
        return Response(data=films_json)
    elif request.method == 'POST':
        with transaction.atomic():
            # Step 0. Validation
            serializer = FilmCreateValidateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'message': 'Request failed',
                                      'errors': serializer.errors})

            # Step 1. Get data from validated data
            genres = serializer.validated_data.get('genres')

            # Step 2. Create Film with data
            film = Film.objects.create(**serializer.create_validated_data())
            film.genres.set(genres)
            film.save()

            # Step 3. Return response (status) as created object
            return Response(status=status.HTTP_201_CREATED,
                            data={'message': "Film created",
                                  'film': {'id': film.id, 'title': film.title}})


@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, film_id):
    try:
        film = Film.objects.select_related('director').prefetch_related('reviews').get(id=film_id)
    except Film.DoesNotExist:
        return Response(data={'message': 'Film not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        film_json = FilmSerializer(film, many=False).data
        return Response(data=film_json)
    elif request.method == 'PUT':
        serializer = FilmCreateValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        film.title = request.data.get('title')
        film.text = request.data.get('text')
        film.duration = request.data.get('duration')
        film.rating_kinopoisk = request.data.get('rating')
        film.director_id = request.data.get('director_id')
        film.genres.set(request.data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Film updated'})
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'Film Destoyed'})
