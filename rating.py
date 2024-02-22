import pandas as pd 
import numpy as np
from sklearn.preprocessing import StandardScaler 
import random

df_songs = pd.read_csv('spotify_songs.csv')

audio_features = df_songs[['danceability', 'energy', 'loudness', 
                           'mode', 'speechiness', 'acousticness',
                           'instrumentalness', 'valence', 'tempo']].to_numpy()

scaler = StandardScaler() # Create a scaler object
normalized_features = scaler.fit_transform(audio_features) 
ratings = []

NUM_RATING_SONGS = 2
random_indices = random.sample(range(len(df_songs)), NUM_RATING_SONGS)

for index in random_indices: # Iterate through CSV rows
    track_name = df_songs.loc[index, 'track_name']
    track_artist = df_songs.loc[index, 'track_artist']

    print(f"Song: {track_name} by {track_artist}")
    rating = int(input("Enter your rating (1-10): "))

    while rating < 1 or rating > 10:
        print("Invalid rating. Please enter a number between 1 and 10.")
        rating = int(input("Enter your rating (1-10): "))

    features = normalized_features[index]  # Use normalized features
    ratings.append({'features': features, 'rating': rating}) 

# Create a DataFrame from the ratings data
ratings_df = pd.DataFrame(ratings)
ratings_df.to_csv('song_ratings.csv', index=False) 


