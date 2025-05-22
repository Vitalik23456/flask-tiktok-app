from flask import Flask, request, render_template, redirect, url_for, jsonify
import sqlite3
import requests
import os
app = Flask(__name__)
DATABASE = 'users.db'

def get_db():
    return sqlite3.connect(DATABASE)

def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            video_url TEXT,
            mp4_url TEXT
        )
    ''')
    conn.commit()
    conn.close()
create_table()
def get_mp4_link(tiktok_url):
    try:
        res = requests.get("https://tikwm.com/api/", params={"url": tiktok_url})
        data = res.json()
        return data["data"]["play"] if data["data"] and data["data"]["play"] else None
    except:
        return None

@app.route('/')
def home():
    user_id = request.args.get('user_id')
    return render_template('index.html', user_id=user_id)

@app.route('/add_video/<user_id>', methods=['GET', 'POST'])
def add_video(user_id):
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        if video_url:
            mp4_link = get_mp4_link(video_url)
            if not mp4_link:
                return "Помилка: не вдалося отримати пряме посилання на відео", 400

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (user_id, video_url, mp4_url) VALUES (?, ?, ?)",
                (user_id, video_url, mp4_link)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('home', user_id=user_id))
    return render_template('add_video.html', user_id=user_id)

@app.route('/api/videos')
def api_videos():
    user_id = request.args.get('user_id')
    conn = get_db()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT mp4_url FROM users WHERE user_id = ?", (user_id,))
    else:
        cursor.execute("SELECT mp4_url FROM users")
    raw_urls = cursor.fetchall()
    conn.close()

    result = [row[0] for row in raw_urls if row[0]]

    return jsonify(result)
conn = get_db()
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(users);")
columns = cursor.fetchall()
conn.close()
print(columns)
[(0, 'id', 'INTEGER', 0, None, 1), (1, 'user_id', 'TEXT', 0, None, 0), ...]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    

