import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import StandardScaler
from flask import Flask, render_template, url_for, jsonify, request
from database import get_db_connection, create_ratings_table, insert_rating 
from song import get_song_data, df_songs, current_song_index


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_first_song')  # New route
def get_first_song():
    global current_song_index
    song = get_song_data(current_song_index) 
    return jsonify(song)

create_ratings_table()

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    print("inside submit_rating")
    rating = int(request.form['rating'])  # Ensure rating is an integer
    next_song_index = random.randint(0, len(df_songs) - 1) 
    next_song = get_song_data(next_song_index)
    song_id = request.form['songId'] 

    conn = get_db_connection()
    cursor = conn.cursor()
    insert_rating(song_id, rating)
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'next_song': next_song  # Make sure 'next_song' includes the 'id'
    })

if __name__ == '__main__':
    app.run(debug=True)