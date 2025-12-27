# 🎬 Mood‑Based Movie Recommender

A simple **content‑based movie recommendation app** built with Python, scikit‑learn, and Streamlit.  
Users describe how they feel (e.g., _“I am sad and need something to cheer me up”_) and the app suggests movies that match their mood and preferences.

The app uses the **MovieLens 100k** movies metadata and a **TF‑IDF + cosine similarity** model over titles and genres to find relevant movies. 

---

## ✨ Features

- **Free‑text mood prompts**  
  Type what you feel or what kind of movie you want (e.g., _“I want a romantic comedy that is light and funny”_).

- **Content‑based recommendations**  
  Uses TF‑IDF vectorization over `title + genres` and cosine similarity to find movies whose content best matches your prompt. 

- **Genre filters**  
  Optional multiselect to restrict results to specific genres (e.g., `Comedy`, `Action`, `Romance`).

- **Exclude already‑seen movies**  
  Enter a comma‑separated list of titles you’ve already watched; the app removes them from recommendations.

- **Interactive web UI (Streamlit)**  
  A slider to control how many recommendations to search, and a table of matching movies.

---

## 🗂️ Dataset

This project uses the **MovieLens 100k** movies metadata: 

- `movies.csv` (columns: `movieId`, `title`, `genres`)
- Other MovieLens files (`ratings.csv`, `tags.csv`, `links.csv`) are not used in the current version.

Place `movies.csv` in the project folder.


---

## 🧠 How it works (Model)

1. **Content representation**

In `recommender.py`:

- Load `movies.csv` into a pandas DataFrame.
- Clean the `genres` column and create a `content` string:

  ```
  movies['content'] = movies['title'] + " " + movies['genres'].str.replace('|', ' ', regex=False)
  ```

2. **TF‑IDF vectorization**

- Use `TfidfVectorizer(stop_words='english')` to convert `content` into a TF‑IDF matrix. 
- Each movie becomes a vector in a high‑dimensional space.

3. **Prompt‑based similarity**

- The user’s prompt is transformed into a TF‑IDF vector using the same vectorizer.
- Cosine similarity between the prompt vector and each movie vector is computed.
- Top‑N movies with the highest similarity scores are recommended.

4. **Filters and exclusions**

- **Genre filter**: only keep movies whose `genres` contain at least one of the selected genres.
- **Already‑seen list**: drop any movies whose titles match the list provided by the user.

---

### App workflow

1. Enter a prompt describing your mood or desired movie type.  
2. (Optional) Select one or more genres to filter by.  
3. (Optional) Enter titles you’ve already seen (comma-separated).  
4. Choose how many recommendations to search for using the slider.  
5. Click **“Recommend”** to see a table of suggested movies.

---

## 🚀 Possible Future Improvements

- Switch from `title + genres` to a dataset with **plot/overview text** (e.g., TMDb/IMDB) to better understand mood and story content. 
- Add year, rating, or language filters.
- Integrate a real movie API (TMDb) to display posters, overviews, and more metadata.
- Log user feedback (like/dislike) to refine recommendations over time or build a hybrid (content + collaborative) recommender. 

---

## 📚 References

- MovieLens dataset (GroupLens).
- TF‑IDF and cosine similarity for content-based movie recommenders. 



