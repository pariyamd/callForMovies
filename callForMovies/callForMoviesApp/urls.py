from django.urls import path
from . import views
urlpatterns=[
    path("",views.home),
    path("movie_detail/<int:pk>",views.submit_comment, name='movie_detail')
    ]