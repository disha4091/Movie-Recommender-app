import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d9b66e7052a5521a822726b5f5b1d8e4&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie,no_of_movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x : x[1])[1:no_of_movie+1]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movies_poster


movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('movie recommender system!')

selected_movie = st.selectbox(
    'Select a movie',movies['title'].values
)

no_of_movie = st.selectbox(
    'Select number of movies to be recommended', [1,2,3,4,5]
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie,no_of_movie)
    for i in range(0,no_of_movie):
        st.header(names[i])
        st.image(posters[i])
