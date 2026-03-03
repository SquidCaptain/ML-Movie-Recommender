import pickle
import numpy as np
import scipy.sparse as sp
from sklearn.metrics.pairwise import linear_kernel

from .models import Movie


# Load once at startup
tfidf = pickle.load(open("../../model/tfidf.pkl", "rb"))
svd_model = pickle.load(open("../../model/svd_model.pkl", "rb"))
indices = pickle.load(open("../../model/indices.pkl", "rb"))
tfidf_matrix = sp.load_npz("../../model/tfidf_matrix.npz")

# Build reverse index once
index_to_movieId = {
    v: k for k, v in indices.items()
}


def recommend_from_favorites(favorite_titles, top_n=10):
    if not favorite_titles:
        return Movie.objects.none()

    sim_scores = np.zeros(tfidf_matrix.shape[0])

    for title in favorite_titles:
        if title in indices:
            idx = indices[title]
            sim = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
            sim_scores += sim

    sim_scores /= len(favorite_titles)

    top_indices = np.argsort(sim_scores)[::-1][1:top_n+1]

    recommended_movieIds = [
        index_to_movieId[i] for i in top_indices
    ]

    return Movie.objects.filter(movieId__in=recommended_movieIds)


def recommend_hybrid(user_id, favorite_title, top_n=10):
    if favorite_title not in indices:
        return Movie.objects.none()

    idx = indices[favorite_title]

    sim_scores = linear_kernel(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    candidate_indices = np.argsort(sim_scores)[::-1][1:top_n * 5]

    scores = []

    for i in candidate_indices:
        movie_id = index_to_movieId[i]

        collab_score = svd_model.predict(user_id, movie_id).est
        content_score = sim_scores[i]

        final_score = 0.5 * content_score + 0.5 * collab_score
        scores.append((movie_id, final_score))

    scores.sort(key=lambda x: x[1], reverse=True)

    final_movieIds = [m[0] for m in scores[:top_n]]

    return Movie.objects.filter(movieId__in=final_movieIds)