import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("datasets/movies.csv")

movies['genres'] = movies['genres'].replace('(no genres listed)', '')

movies['content'] = movies['title'] + " " + movies['genres'].str.replace('|', ' ', regex=False)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['content'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

movies = movies.reset_index(drop=True)

def recommend_from_prompt(prompt: str, n: int = 10) -> pd.DataFrame:
    """
    Recommend n movies based on a free-text prompt (mood/description),
    using the same TF-IDF vectorizer and cosine similarity.

    Returns a pandas DataFrame with at least: title, genres.
    """
    prompt = prompt.strip()
    if not prompt:
        return pd.DataFrame(columns=['title', 'genres'])

    prompt_vec = tfidf.transform([prompt])

    sim_scores = cosine_similarity(prompt_vec, tfidf_matrix).flatten()

    top_indices = sim_scores.argsort()[::-1][:n]

    return movies.loc[top_indices, ['title', 'genres']]

def get_all_genres():
    """
    Return a sorted list of unique genres from the dataset.
    """
    all_genres = set()
    for g in movies['genres']:
        if isinstance(g, str) and g:
            for part in g.split('|'):
                all_genres.add(part.strip())
    return sorted(all_genres)
