import streamlit as st
import pickle
import pandas as pd
import requests


st.title('Movie Recommender System')


def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{0}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id)
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def Recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    l = []
    poster=[]
    for i in movies_list:
        movie_id = movies['id'][i[0]]
        l.append(movies['title'][i[0]])
        poster.append(fetch_poster(movie_id))
    return l,poster


movie_list = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_list)

similarity = pickle.load(open('similarity.pkl','rb'))

Selected_movie_name = st.selectbox(
'Choose a movie name',
(movies['title'].values))

if st.button('Recommend'):
    Names,posters =Recommend(Selected_movie_name)
    cols = st.columns(5)

    with st.container():
        for i in range(5):
            cols[i].image(posters[i], use_container_width=True)
            cols[i].write(Names[i])