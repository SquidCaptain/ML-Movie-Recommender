from django.shortcuts import render
from .models import Movie
from .recommender import recommend_from_favorites

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