from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path("generate-grid", views.gen_grid)
]