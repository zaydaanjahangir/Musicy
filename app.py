import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask import Flask, render_template, url_for, jsonify

df_songs = pd.read_csv('spotify_songs.csv')
feature_cols = ['danceability', 'energy', 'loudness', 'mode', 'speechiness', 
                'acousticness', 'instrumentalness', 'valence', 'tempo']

scaler = StandardScaler()
normalized_features = scaler.fit_transform(df_songs[feature_cols])


def get_song_data(index):
    song_dict = {
        'title': df_songs.loc[index, 'track_name'],
        'artist': df_songs.loc[index, 'track_artist'],
        'id':df_songs.loc[index, 'track_id'],
        'features': normalized_features[index]
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

