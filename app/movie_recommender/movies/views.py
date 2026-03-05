from django.shortcuts import render, redirect
from .models import Movie, Rating
from .recommender import recommend_from_favorites, recommend_hybrid
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def home(request):
    movies = Movie.objects.all()[:20]
    return render(request, "home.html", {"movies": movies})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after register
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})

def recommend(request):
    if request.method == "POST":
        favorites = request.POST.getlist("favorites")
        recommendations = recommend_from_favorites(favorites)
        return render(request, "recommend.html", {"recommendations": recommendations})
    movies = Movie.objects.all()
    return render(request, "recommend_form.html", {"movies": movies})

@login_required
def recommend_user(request):
    user_ratings = Rating.objects.filter(user=request.user, rating__gte=4)

    if not user_ratings.exists():
        return render(request, "recommend.html", {"recommendations": []})

    favorite_movie = user_ratings.first().movie.title

    recommendations = recommend_hybrid(
        user_id=request.user.id,
        favorite_title=favorite_movie
    )

    return render(request, "recommend.html", {"recommendations": recommendations})

def search_movies(request):
    query = request.GET.get("q", "")

    if len(query) < 2:
        return JsonResponse([], safe=False)

    movies = (
        Movie.objects
        .filter(title__icontains=query)
        .only("id", "title", "poster_path")
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

@login_required
def rate_movie(request):
    if request.method == "POST":
        movie_id = request.POST.get("movie_id")
        rating_value = float(request.POST.get("rating"))

        movie = Movie.objects.get(id=movie_id)

        Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={"rating": rating_value}
        )

        return JsonResponse({"status": "success"})