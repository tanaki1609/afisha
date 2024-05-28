from django.urls import path
from films import views

urlpatterns = [
    path('', views.films_list_api_view),
    path('<int:id>/', views.films_detail_api_view),
]