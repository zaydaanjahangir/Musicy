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
    result = df_songs[df_songs['track_artist'].str.contains(artist_name, case=True, na=False)]
    result_track_names = result[['track_name', 'track_artist']]
    print(result_track_names)

def find_most_similar_song(new_song_features, all_song_features, metric='cosine'):
    """ Finds the most similar song from a subset of songs.

    Args:
        new_song_features: Audio features of the target song.
        all_song_features:  NumPy array of features for your entire song dataset.
        metric: 'cosine' or 'euclidean' for similarity comparison.

    Returns:
        The index of the most similar song within the subset.
    """

    most_similar_index = None
    max_similarity = -float('inf')  # Initial value to ensure any comparison exceeds it

    # Iterate through a subset (first 10 songs in this case)  
    for index, song_features in enumerate(all_song_features[:30000]): 

        similarity = calculate_simlarity(new_song_features, song_features, metric)
        if similarity != 1.0:
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_index = index
    print (similarity)
    return most_similar_index


df_songs = pd.read_csv('spotify_songs.csv')
audio_features = df_songs[['danceability', 'energy', 'loudness', 'mode', 'speechiness', 'acousticness',
                           'instrumentalness', 'valence', 'tempo']].to_numpy()
scaler = StandardScaler()
normalized_features = scaler.fit_transform(audio_features) # Normalizes numerical features to standardize them all

song1_features = normalized_features[1729]
# song2_features = normalized_features[370]
# similarity = calculate_similarity_linalg(song1_features, song2_features, 'cosine')

most_similar_index = find_most_similar_song(song1_features, normalized_features)
recommended_song = df_songs.iloc[most_similar_index][['track_name', 'track_artist']]
#print(find_artist('One Direction'))
print(recommended_song)
