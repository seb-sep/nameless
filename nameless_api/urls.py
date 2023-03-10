from django.urls import path
from . import views

urlpatterns = [
    path("", views.getData),
    path("search/teacher/<str:name>", views.)
]