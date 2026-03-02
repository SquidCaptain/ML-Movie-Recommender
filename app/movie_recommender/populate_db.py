import pandas as pd
from tqdm import tqdm
from movies.models import Movie

df = pd.read_csv("../../data/processed/movies_enriched.csv")

for _, row in tqdm(df.iterrows()):
    Movie.objects.get_or_create(
        movieId=row["movieId"],
        defaults={
            "tmdbId": row["tmdbId"],
            "title": row["title"],
            "genres": row["genres"],
            "keywords": row["keywords"],
            "overview": row["overview"],
            "directors": row["directors"],
            "actors": row["actors"],
            "poster_path": row["poster_path"],
        }
    )

print("Movies loaded!")