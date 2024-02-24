import pandas as pd
import sqlite3
import random
from sklearn.preprocessing import StandardScaler
from flask import Flask, render_template, url_for, jsonify, request


df_songs = pd.read_csv('spotify_songs.csv')
feature_cols = ['danceability', 'energy', 'loudness', 'mode', 'speechiness', 
                'acousticness', 'instrumentalness', 'valence', 'tempo']
scaler = StandardScaler()
normalized_features = scaler.fit_transform(df_songs[feature_cols])

def get_db_connection():
    conn = sqlite3.connect('music_ratings.db')
    return conn

def create_ratings_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_id TEXT,
            rating INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Initialization (Call this once at app start)
create_ratings_table() 
    
def get_song_data(index):
    song_dict = {
        'title': df_songs.loc[index, 'track_name'],
        'artist': df_songs.loc[index, 'track_artist'],
        'id':df_songs.loc[index, 'track_id'],
        'features': normalized_features[index].tolist()
    }
    print(f"Song Data: {song_dict}")  # Add this print statement
    return song_dict

current_song_index = 0
ratings = [] 

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_first_song')  # New route
def get_first_song():
    global current_song_index
    song = get_song_data(current_song_index) 
    return jsonify(song)

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    print("inside submit_rating")
    rating = int(request.form['rating'])  # Ensure rating is an integer
    next_song_index = random.randint(0, len(df_songs) - 1) 
    next_song = get_song_data(next_song_index)
    song_id = request.form['songId'] 

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ratings (song_id, rating) VALUES (?, ?)",
                   (song_id, rating))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'next_song': next_song  # Make sure 'next_song' includes the 'id'
    })

if __name__ == '__main__':
    app.run(debug=True)