import pickle

from flask import Flask, request, app, jsonify, url_for, render_template
import requests
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
      movie_details = get_movie_details(movies.iloc[item[0]].movie_id)
      # movie_list.append({
      #     "name": movies.iloc[item[0]].title,
      #     "poster": get_poster(movies.iloc[item[0]].movie_id)
      # })
      movie_details['name'] = movies.iloc[item[0]].title
      movie_list.append(movie_details)
  return movie_list

def get_movie_details(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=1d4848b17b678e542fd9e959d96d3648".format(movie_id))
    data = response.json()
    genres = []
    for genre in data['genres']:
        genres.append(genre['name'])
    movie_data = {
        'poster': "https://image.tmdb.org/t/p/w500{}".format(data["backdrop_path"]),
        'genres':genres,
        'overview': ' '.join(data['overview'].split()[:30]),
        'tagline':data['tagline'],
    }
    return movie_data



if __name__ == "__main__":
    app.run(debug=True)
