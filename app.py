import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=96a816978b6a3613c62a9aab7557d9d5&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path


def fetch_link(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=96a816978b6a3613c62a9aab7557d9d5&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    mo_id = data['id']
    movie_title = data['original_title']

    full_link = "https://www.themoviedb.org/movie/" + str(mo_id)+"-" + movie_title.replace(" ", "-").lower()
    return full_link


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_link = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_link.append(fetch_link(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters, recommended_movie_link


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Please Select the Movie',
    movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_link = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        # st.image(recommended_movie_posters[0])
        image_width=100
        st.markdown(f'<a href="{recommended_movie_link[0]}" target="_blank"><img src="{recommended_movie_posters[0]} "  width=100px  ></a>', unsafe_allow_html=True)
    with col2:
        st.text(recommended_movie_names[1])
        # st.image(recommended_movie_posters[1])
        st.markdown(
            f'<a href="{recommended_movie_link[1]}" target="_blank"><img src="{recommended_movie_posters[1]} "  width=100px  ></a>',
            unsafe_allow_html=True)

    with col3:
        st.text(recommended_movie_names[2])
        # st.image(recommended_movie_posters[2])
        st.markdown(
            f'<a href="{recommended_movie_link[2]}" target="_blank"><img src="{recommended_movie_posters[2]} " width=100px ></a>',
            unsafe_allow_html=True)
    with col4:
        st.text(recommended_movie_names[3])
        # st.image(recommended_movie_posters[3])
        st.markdown(
            f'<a href="{recommended_movie_link[3]}" target="_blank"><img src="{recommended_movie_posters[3]} "  width=100px ></a>',
            unsafe_allow_html=True)
    with col5:
        st.text(recommended_movie_names[4])
        # st.image(recommended_movie_posters[4])
        st.markdown(
            f'<a href="{recommended_movie_link[4]}" target="_blank"><img src="{recommended_movie_posters[4]}" width=100px ></a>',
            unsafe_allow_html=True)

