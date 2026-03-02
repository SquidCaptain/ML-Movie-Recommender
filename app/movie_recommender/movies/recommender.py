import pickle
import numpy as np
import scipy.sparse as sp
from sklearn.metrics.pairwise import cosine_similarity

from .models import Movie

# Load models once at startup
tfidf = pickle.load(open("../../model/tfidf.pkl", "rb"))
svd_model = pickle.load(open("../../model/svd_model.pkl", "rb"))
indices = pickle.load(open("../../model/indices.pkl", "rb"))
tfidf_matrix = sp.load_npz("../../model/tfidf_matrix.npz")

def recommend_from_favorites(favorite_titles, top_n=10):
    sim_scores = np.zeros(tfidf_matrix.shape[0])

    for title in favorite_titles:
        if title in indices:
            idx = indices[title]
            sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
            sim_scores += sim

    sim_scores = sim_scores / len(favorite_titles)

    top_indices = np.argsort(sim_scores)[::-1][1:top_n+1]

    movie_ids = Movie.objects.values_list('movieId', flat=True)
    return Movie.objects.filter(movieId__in=[list(movie_ids)[i] for i in top_indices])

def recommend_hybrid(user_id, favorite_title, top_n=10):
    if favorite_title not in indices:
        return []

    idx = indices[favorite_title]

    sim_scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    candidate_indices = np.argsort(sim_scores)[::-1][1:top_n*5]

    scores = []
    movie_ids = list(Movie.objects.values_list('movieId', flat=True))

    for i in candidate_indices:
        movie_id = movie_ids[i]

        collab = svd_model.predict(user_id, movie_id).est
        content = sim_scores[i]

        final = 0.5 * content + 0.5 * collab
        scores.append((movie_id, final))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]

    return Movie.objects.filter(movieId__in=[m[0] for m in scores])