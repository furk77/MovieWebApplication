import requests
import textblob
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
app = Flask(__name__)

load_dotenv('env/secrets.env')
# TMDb API Key
API_KEY = os.getenv('MOVIE_KEY')

def get_movie_data(movie_name):
    """Fetch movie data from TMDb API."""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []

# Home route
@app.route('/')
def index():
    return render_template('index.html')

def analyze_sentiment(text):
    blob = textblob.TextBlob(text)
    return blob.sentiment
# Search route
@app.route('/search', methods=['POST'])
def search():
    movie_name = request.form['movie_name']
    movies = get_movie_data(movie_name)
    
    # Analyze sentiment for each movie overview
    for movie in movies:
        overview = movie.get('overview', '')
        sentiment = analyze_sentiment(overview)
        movie['polarity'] = round(sentiment.polarity, 2)  
        movie['subjectivity'] = round(sentiment.subjectivity, 2)  
    
    # Pass movies with sentiment data to the template
    return render_template('results.html', movie_name=movie_name, movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
