from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', views.recommend, name='recommend'),
    path("recommend-user/", views.recommend_user, name="recommend_user"),
    path('search/', views.search_movies, name='search_movies'),

    path('ratings/', views.ratings_page, name='ratings_page'),
    path('rate/', views.rate_movie, name='rate_movie'),

    path('register/', views.register, name='register'),
]