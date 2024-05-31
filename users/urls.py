from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration_api_view),
    path('authorization/', views.AuthorizationAPIView.as_view()),
]