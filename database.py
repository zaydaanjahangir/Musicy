import sqlite3
import pandas as pd

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

def insert_rating(song_id, rating):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ratings (song_id, rating) VALUES (?, ?)",
                   (song_id, rating))
    conn.commit()
    conn.close()

def load_ratings_from_database():
    conn = sqlite3.connect('music_ratings.db')
    ratings_df = pd.read_sql_query("SELECT song_id, rating FROM ratings", conn) 
    conn.close()
    return ratings_df

