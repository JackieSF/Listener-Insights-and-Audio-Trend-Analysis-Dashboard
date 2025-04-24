from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
import google.generativeai as genai
from inventory import inventory
from ai import customers

load_dotenv()

# Setup Flask app
app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/events')
def get_events():
    return jsonify(inventory)

@app.route('/api/customers')
def get_customers():
    return jsonify(customers)

@app.route('/api/event_insight/<event_id>')
def get_event_insight(event_id):
    event = next((e for e in inventory if e['id'] == event_id), None)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    # Find customers interested in similar genres/artists
    matched_customers = [c for c in customers if
                         set(event['genres']).intersection(c['top_genres']) or
                         set(event['artists']).intersection(c['top_artists'])]

    prompt = f"""
    Analyze the following event and customer data. Describe the vibe of the event, who it's for, what music is featured,
    and include suggestions on audience targeting.

    Event: {event}
    Matched Customers: {matched_customers[:5]}  # Just send a few sample customers for speed
    """

    response = model.generate_content(prompt)
    return jsonify({'insight': response.text})

if __name__ == '__main__':
    app.run(debug=True)