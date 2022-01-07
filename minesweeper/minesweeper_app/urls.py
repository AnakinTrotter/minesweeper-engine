from django.urls import path
from . import views
# notes for KAM: similar to routing, calls stuff in views.py

urlpatterns = [
    path('', views.index),
    path('test/', views.test),
    path("generate", views.gen_grid)
]