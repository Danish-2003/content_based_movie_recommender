import streamlit as st
import pickle
import pandas as pd
import requests


# Content Based Recommendation system

# Model  and data
movie_names = pickle.load(open('data/movie_dict.pkl','rb'))

similarity = pickle.load(open('data/similarity.pkl','rb'))

movies = pd.DataFrame(movie_names)


#Functionalities

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a9ef27ee6f268146754ebb61e8e02c60&external_source=imdb_id'.format(movie_id))
    data = response.json()
    
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w185/" + data['poster_path']
    else:
        return "https://via.placeholder.com/185"


def recommend(movie):
    
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    
    for i in movie_list:
        
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster
    



# Development Content

st.title("Movie Recommender System")

selected_movie = st.selectbox(
    "Get the movie recommendations",
    (movies['title'].values),
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie)
    
    col = st.columns(5)
    for i in range(5):
        
        with col[i]:
            st.text(names[i])
            st.image(posters[i])
    