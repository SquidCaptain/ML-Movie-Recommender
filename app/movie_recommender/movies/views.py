from django.shortcuts import render
from .models import Movie
from .recommender import recommend_from_favorites
from django.http import JsonResponse
from django.db.models import Q

def home(request):
    movies = Movie.objects.all()[:20]
    return render(request, "home.html", {"movies": movies})

def recommend(request):
    if request.method == "POST":
        favorites = request.POST.getlist("favorites")
        recommendations = recommend_from_favorites(favorites)
        return render(request, "recommend.html", {"recommendations": recommendations})
    movies = Movie.objects.all()
    return render(request, "recommend_form.html", {"movies": movies})

def search_movies(request):
    query = request.GET.get("q", "")

    if len(query) < 2:
        return JsonResponse([], safe=False)

    movies = (
        Movie.objects
        .filter(title__icontains=query)
        .only("id", "title", "poster_path")  # 👈 important
        [:10]
    )

    data = [
        {
            "id": movie.id,
            "title": movie.title,
            "poster": movie.poster_path,
        }
        for movie in movies
    ]

    return JsonResponse(data, safe=False)