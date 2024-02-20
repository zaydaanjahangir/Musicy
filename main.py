import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine, euclidean
from sklearn.preprocessing import StandardScaler

def calculate_simlarity(song1_features, song2_features, metric):
    if metric == 'cosine':
        return 1 - cosine(song1_features, song2_features)
    elif metric == 'euclidean':
        return euclidean(song1_features, song2_features)
    else:
        raise ValueError("Invalid similarity metric")

def calculate_similarity_linalg(song1_features, song2_features, metric):
    if metric == 'cosine':
        dot_product = np.dot(song1_features, song2_features)
        norm_a = np.linalg.norm(song1_features)
        norm_b = np.linalg.norm(song2_features)
        return dot_product / (norm_a * norm_b)
    elif metric == "euclidean":
        return np.linalg.norm(song1_features - song2_features)
    else:
        raise ValueError("Invalid similarity metric")

def find_artist(artist_name):
    result = df_songs[df_songs['track_artist'].str.contains('track_artist', case=True, na=False)]
    result_track_names = result[['track_name', 'track_artist']]
    return result_track_names


df_songs = pd.read_csv('/Users/zayj/Desktop/projects/musicy/Music/spotify_songs.csv')
audio_features = df_songs[['danceability', 'energy', 'loudness', 'mode', 'speechiness', 'acousticness',
                           'instrumentalness', 'valence', 'tempo']].to_numpy()
scaler = StandardScaler()
normalized_features = scaler.fit_transform(audio_features) # Normalizes numerical features to standardize them all


# track_id = '145'
# song1 = df_songs.iloc[145][audio_features].values