from django.urls import path
from . import views

urlpatterns = [
    path("", views.getData),
    path("search/teacher/<str:name>", views.searchTeacher),
    path("search/course/<str:name>", views.searchCourse),
    path("teacher/<email:pk>", views.getTeacher),
]