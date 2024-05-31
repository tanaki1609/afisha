from django.urls import path
from films import views

urlpatterns = [
    path('', views.FilmListCreateAPIView.as_view()),
    path('<int:id>/', views.films_detail_api_view),
    path('directors/', views.DirectorListCreateAPIView.as_view()),  # GET->list, # POST->create
    path('directors/<int:id>/',
         views.DirectorItemAPIView.as_view()),  # GET->retrieve, PUT->update, DELETE->destroy
    path('tags/', views.TagModelViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('tags/<int:id>/', views.TagModelViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    }))
]
