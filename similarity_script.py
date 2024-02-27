import pandas as pd 
import numpy as np
from database import load_ratings_from_database

def calculate_similarity(song1_id, song2_id, ratings_df):
        ratings_song1 = ratings_df[ratings_df['song_id'] == song1_id]['rating'].to_numpy()
        ratings_song2 = ratings_df[ratings_df['song_id'] == song2_id]['rating'].to_numpy()

        # Handle cases where not enough ratings exist for both songs
        if ratings_song1.size == 0 or ratings_song2.size == 0:
            return 0  # No rating exists for one or both songs 

        # If ratings arrays are identical, correlation is technically 1
        if np.array_equal(ratings_song1, ratings_song2):  
            return 1

        # Otherwise, calculate correlation as before
        return np.corrcoef(ratings_song1, ratings_song2)[0, 1]

def find_similar_songs(similarity_threshold):
    ratings_df = load_ratings_from_database()
    similar_pairs = []
    rated_song_ids = ratings_df['song_id'].unique()

    for i in range(len(rated_song_ids)):
        for j in range(i + 1, len(rated_song_ids)):
            similarity = calculate_similarity(rated_song_ids[i], rated_song_ids[j], ratings_df)
            if similarity > similarity_threshold:
                similar_pairs.append((rated_song_ids[i], rated_song_ids[j]))
    
    return similar_pairs


similar_pairs = find_similar_songs(similarity_threshold=0.7)
print(similar_pairs)