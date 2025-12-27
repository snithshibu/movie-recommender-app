import streamlit as st
from recommender import recommend_from_prompt, get_all_genres, movies

st.set_page_config(page_title="Mood-based Movie Recommender", page_icon="🎬")

st.title("🎬 Mood-based Movie Recommender")
st.write(
    "Describe how you feel or what kind of movie you want, "
    "and get movie suggestions based on your mood and preferences."
)

st.markdown(
    """
    **Examples of prompts:**
    - "I am sad and need something to cheer me up"
    - "I feel bored and want a fun action movie"
    - "I want a romantic comedy that is light and funny"
    """
)

# Prompt input
prompt = st.text_area(
    "How are you feeling today, or what kind of movie do you want?",
    placeholder="Example: I am sad and need something to cheer me up"
)

# Genre filter
all_genres = get_all_genres()
selected_genres = st.multiselect(
    "Filter by genres (optional):",
    options=all_genres,
    help="If you select one or more genres, only movies that contain at least one of these genres will be shown."
)

# Already seen titles
seen_titles_input = st.text_area(
    "Movies you've already seen (optional, comma-separated titles):",
    placeholder="Example: Toy Story (1995), Jumanji (1995)"
)

# Number of recommendations
n_recs = st.slider(
    "Number of recommendations to search for (before filters):",
    min_value=5,
    max_value=50,
    value=20,
    step=5,
    help="The app finds this many top matches first, then applies your filters."
)

if st.button("Recommend"):
    if not prompt.strip():
        st.warning("Please enter a prompt describing your mood or what kind of movie you want.")
    else:
        # Step 1: get initial recommendations from prompt
        results = recommend_from_prompt(prompt, n=n_recs)

        # Step 2: apply genre filter if any
        if selected_genres:
            mask = results['genres'].apply(
                lambda g: any(gen in g.split('|') for gen in selected_genres)
            )
            results = results[mask]

        # Step 3: exclude already-seen titles
        seen_titles = []
        if seen_titles_input.strip():
            seen_titles = [t.strip() for t in seen_titles_input.split(',') if t.strip()]
            if seen_titles:
                results = results[~results['title'].isin(seen_titles)]

        if results.empty:
            st.warning(
                "No recommendations found after applying your filters. "
                "Try a different prompt, relax the genre filters, or remove some 'already seen' titles."
            )
        else:
            st.subheader("Recommended movies for your mood:")
            st.write(f"Found {len(results)} movies matching your prompt and filters.")

            st.dataframe(results.reset_index(drop=True))

st.markdown(
    """
    ---
    **How it works**

    This app uses a simple content-based recommendation approach:

    - It builds a text representation of each movie using its title and genres.
    - Your prompt is converted into a TF-IDF vector using the same vocabulary.
    - The similarity between your prompt and each movie is computed using cosine similarity.
    - The most similar movies are recommended, and then optional genre and 'already seen' filters are applied.
    """
)

st.caption(
    """
    ---
    Done by Snith Shibu. I was bored lol.
    """
)
