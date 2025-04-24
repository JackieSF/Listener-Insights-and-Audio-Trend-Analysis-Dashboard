from flask import Flask, redirect, request, session, url_for, render_template, render_template, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import requests
from inventory import inventory
from customers import customers


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify auth manager setup
sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read user-top-read user-read-recently-played"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    session["token_info"] = token_info
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_profile = sp.current_user()
    return f"<h1>Welcome, {user_profile['display_name']}!</h1>"

@app.route("/inventory")
def get_inventory():
    return jsonify({"inventory": inventory})

@app.route("/curated-audience/<event_id>")
def curated_audience(event_id):
    event = next((e for e in inventory if e["id"] == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    audience = []
    for customer in customers:
        genre_match = len(set(event["genres"]) & set(customer["top_genres"]))
        artist_match = len(set(event["artists"]) & set(customer["top_artists"]))
        match_confidence = (genre_match + artist_match) / (len(event["genres"]) + len(event["artists"]))
        
        if match_confidence > 0:
            audience.append({
                "name": customer["name"],
                "location": customer["location"],
                "top_genres": customer["top_genres"],
                "top_artists": customer["top_artists"],
                "recent_tracks": customer["recent_tracks"],
                "match_confidence": match_confidence,
                "match_reason": f"{genre_match} genre matches, {artist_match} artist matches"
            })

    sorted_audience = sorted(audience, key=lambda x: x["match_confidence"], reverse=True)
    return jsonify({"audience": sorted_audience[:10]})

@app.route("/recommendations")
def get_recommendations():
    recommendations = []
    for event in inventory:
        matching_customers = [
            customer for customer in customers
            if event["genre"] in customer["preferred_genres"]
        ]
        recommendations.append({
            "event": event["name"],
            "matched_customers": [c["name"] for c in matching_customers]
        })
    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(debug=True)


