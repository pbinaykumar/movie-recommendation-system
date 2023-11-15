import pickle

from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movies = pd.DataFrame(movie_dict)

@app.route('/',methods=['GET','POST'])
def home():
    recommended_movies = []
    selected_movie = ""
    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        recommended_movies = recommend(selected_movie)
    return render_template('home.html',all_movie=movies['title'].values,selected_movie=selected_movie,recommended_movies=recommended_movies)

def recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]
  distances = similarity[movie_index]
  movie_index_list = sorted(list(enumerate(distances)),key=lambda x: x[1],reverse=True)[1:6]
  movie_list = []
  for item in movie_index_list:
    movie_list.append(movies.iloc[item[0]].title)
  return movie_list



if __name__ == "__main__":
    app.run(debug=True)
