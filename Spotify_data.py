#importing necessary packages
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load credentials from .env file
load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID"),
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET"),
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

#authenticate & connect to Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-top-read user-library-read"))

#Function to retrieve and process all tracks in a given playlist
def get_playlist_tracks(playlist_id):
    tracks = []
    #Fetch the first batch of tracks from the playlist
    results = sp.playlist_items(playlist_id)
    tracks.extend(results['items'])
    #If more pages of results exist, continue fetching them
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    #Simplify and extract only the fields we care about for each track
    simplified = []
    for item in tracks:
        track = item['track']
        if track:
            #Pull name,artist, popularity & audio features for each track: tempo, energy, danceability, valence
            simplified.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'popularity': track['popularity'],
                'tempo': sp.audio_features(track['id'])[0]['tempo'],
                'energy': sp.audio_features(track['id'])[0]['energy'],
                'danceability': sp.audio_features(track['id'])[0]['danceability'],
                'valence': sp.audio_features(track['id'])[0]['valence'],
            })
#Return the cleaned data as a pandas DataFrame
    return pd.DataFrame(simplified)

if __name__ == "__main__":
    playlist_id = '37i9dQZF1DXcBWIGoYBM5M'  # Spotify Top 50 Global
    df = get_playlist_tracks(playlist_id)
    df.to_csv('spotify_top_tracks.csv', index=False)
    print(df.head())
