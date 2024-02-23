import pandas as pd
from flask import Flask, render_template, url_for, jsonify

df_songs = pd.read_csv('spotify_songs.csv')

def get_song_data(index):
    song_dict = {
        'title': df_songs.loc[index, 'track_name'],
        'artist': df_songs.loc[index, 'track_artist'],
        'features': df_songs.loc[index, ['danceability', 'energy', 'loudness', 'mode', 
                                 'speechiness', 'acousticness', 'instrumentalness',
                                 'valence', 'tempo']].to_numpy()
    }
    print(f"Song Data: {song_dict}")  # Add this print statement
    return song_dict

current_song_index = 0
ratings = [] 



app = Flask(__name__)

@app.route('/')
def index():
    global current_song_index
    song = get_song_data(current_song_index)
    print(f"Sending Song Data: {song}")
    return render_template('index.html', song=song)

if __name__ == '__main__':
    app.run(debug=True)

