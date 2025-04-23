# app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import random
import os

from customers import customers
from inventory import inventory


app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at the root
@app.get("/")
def serve_index():
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/customers")
def get_customers():
    return {"customers": customers}

@app.get("/inventory")
def get_inventory():
    return {"inventory": inventory}

def get_random_audience(event_id: str):
    event = next((e for e in inventory if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Randomly pick ten unique customers
    selected_customers = random.sample(customers, 10)

    audience = []
    for customer in selected_customers:
        match_score = round(random.uniform(0.5, 1.0), 4)  # Score between 0.5 and 1.0
        audience.append({
            "customer_id": customer["id"],
            "name": customer["name"],
            "match_confidence": match_score,
            "top_genres": customer["top_genres"],
            "top_artists": customer["top_artists"],
            "recent_tracks": customer["recent_tracks"],
            "location": customer["location"]
        })

    return {
        "event_id": event_id,
        "audience": audience
    }

def get_audience_with_ai(event_id: str):
    pass
@app.get("/curated-audience/{event_id}")
@app.get("/curated-audience/{event_id}")
@app.get("/curated-audience/{event_id}")
def get_curated_audience(event_id: str):
    event = next((e for e in inventory if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    scored_customers = []

    for customer in customers:
        # Calculate base genre score
        shared_genres = set(event["genres"]) & set(customer["top_genres"])
        genre_score = len(shared_genres)

        # Boost score for shared artists
        shared_artists = set(event["artists"]) & set(customer["top_artists"])
        artist_bonus = len(shared_artists) * 1.5

        # Boost score for same location
        location_bonus = 1 if event["location"] == customer["location"] else 0

        total_score = genre_score + artist_bonus + location_bonus

        if total_score == 0:
            continue  # skip customers with zero relevance

        scored_customers.append((customer, total_score, shared_genres, shared_artists, location_bonus))

    # Sort by total score, highest first
    top_matches = sorted(scored_customers, key=lambda x: x[1], reverse=True)[:10]

    audience = []
    for customer, score, shared_genres, shared_artists, location_bonus in top_matches:
        match_confidence = round(min(1.0, 0.5 + score * 0.1), 2)

        # Create reasoning sentence
        reasons = []
        if shared_genres:
            reasons.append(f"likes {', '.join(shared_genres)}")
        if shared_artists:
            reasons.append(f"is a fan of {', '.join(shared_artists)}")
        if location_bonus:
            reasons.append(f"is located in {customer['location']}")
        reason_text = "This customer " + " and ".join(reasons) + "."

        audience.append({
            "customer_id": customer["id"],
            "name": customer["name"],
            "location": customer["location"],
            "top_genres": customer["top_genres"],
            "top_artists": customer["top_artists"],
            "recent_tracks": customer["recent_tracks"],
            "match_confidence": match_confidence,
            "match_reason": reason_text
        })

    return {
        "event_id": event_id,
        "audience": audience
    }

def get_curated_audience(event_id: str):
    #return get_audience_with_ai(event_id)
    return get_random_audience(event_id)