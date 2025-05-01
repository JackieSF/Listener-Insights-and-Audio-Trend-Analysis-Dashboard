import random
import uuid
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyCsS2syOV4xyY9TBDV4MYje5m5REpiWMTA"))

# Base mock data
first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ivan", "Julia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Taylor", "Davis", "Miller", "Wilson"]
genres = ["pop", "rock", "indie", "hip hop", "rap", "r&b", "electronic", "dance", "house", "country", "alternative"]
artists = ["Taylor Swift", "Drake", "Arctic Monkeys", "Billie Eilish", "Kendrick Lamar", "SZA", "Calvin Harris", "Deadmau5", "Daft Punk", "Lizzo", "Ed Sheeran"]
tracks = [
    {"name": "Bad Blood", "artist": "Taylor Swift"},
    {"name": "Hotline Bling", "artist": "Drake"},
    {"name": "505", "artist": "Arctic Monkeys"},
    {"name": "Happier Than Ever", "artist": "Billie Eilish"},
    {"name": "DNA.", "artist": "Kendrick Lamar"},
    {"name": "Good Days", "artist": "SZA"},
    {"name": "Feel So Close", "artist": "Calvin Harris"},
    {"name": "Strobe", "artist": "Deadmau5"},
    {"name": "One More Time", "artist": "Daft Punk"},
    {"name": "About Damn Time", "artist": "Lizzo"},
    {"name": "Shivers", "artist": "Ed Sheeran"}
]
locations = ["New York", "Los Angeles", "Chicago", "San Francisco", "Austin", "Seattle", "Atlanta", "Miami"]

def make_n_customers(n: int):
    generated_customers = []

    for i in range(n):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        top_genres = random.sample(genres, 3)
        top_artists = random.sample(artists, 3)
        recent_tracks = random.sample(tracks, 2)
        location = random.choice(locations)

        customer = {
            "id": f"user_{str(uuid.uuid4())[:8]}",
            "name": name,
            "top_genres": top_genres,
            "top_artists": top_artists,
            "recent_tracks": recent_tracks,
            "location": location
        }

        generated_customers.append(customer)

    return generated_customers

customers = make_n_customers(100)

def generate_event_insight(event):
    prompt = f"""
    Generate an audience insight for the following event:
    Title: {event['title']}
    Genres: {', '.join(event['genres'])}
    Artists: {', '.join(event['artists'])}
    Location: {event['location']}
    Date: {event['date']}

    Include: 
    - Who the target audience is
    - What kind of music and vibe to expect
    - Who would enjoy this
    - Any age restriction suggestions or parental advisories
    """
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text.strip()


