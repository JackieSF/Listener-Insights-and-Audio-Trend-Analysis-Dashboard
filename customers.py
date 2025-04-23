import random
import uuid

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

# Optional: generate sample customers for dev/testing
customers = make_n_customers(100)
