from django.urls import path
from . import views

urlpatterns = [
    path('KBO/', views.index),
    path('KBO/result/', views.post),
]
