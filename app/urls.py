from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home ),
    path('send_image/', views.get_image),
    path('recommendation/', views.recommendation),
]