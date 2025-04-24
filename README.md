🎧 Vibevault — Music Insights Dashboard
Vibevault is a sleek, AI-powered music dashboard that brings together mock customer and event data with Gemini AI to generate deep audience insights. It also showcases trends in music, artist popularity, and genre breakdowns — all in a beautiful, modern UI.

Whether you're a music marketer, analyst, or someone who just loves music, Vibevault helps you discover who's listening, why, and where the vibes are headed.

🚀 Features
AI-powered summaries for each music event using Gemini (Google's generative AI)

Real-time lists of the top 10 songs and artists on Spotify (mock data only for this version)

Regional breakdowns of genre popularity

Clickable event cards with curated audience insights

Scrollable list of music events with descriptions and details

🛠️ How to Launch the App
1. Clone or Download the App

You can download this project from GitHub or clone it using Git.

2. Install Python (if you don’t have it)

Visit the Python website and install the latest version:
https://www.python.org/downloads/

3. Create a Virtual Environment

This step keeps your project’s packages separate from your system’s Python packages.
(Instructions vary slightly depending on your operating system.)

4. Install Required Libraries

After activating the virtual environment, install the required Python packages using the requirements.txt file (listed below).

5. Set Up Environment Variables

Create a file in the root folder of the project called .env. Inside that file, paste this:

GEMINI_API_KEY=your_gemini_api_key_here

You can get your API key by signing up for Gemini at Google's AI platform.

6. Run the App

Once everything is set up, launch the app by running it from the terminal with:

python app.py

Then open your web browser and go to:
http://127.0.0.1:5000

📁 Project File Structure
app.py: the main backend file where routes and API logic live

ai.py: uses Gemini AI to generate audience and vibe summaries

inventory.py: mock data representing music events

customers.py: mock user/customer profiles

templates/index.html: the main HTML layout for the dashboard

static/style.css: styling for the dashboard

static/script.js: handles all frontend interactivity and event loading

.env: contains your API key (not tracked in version control)

📦 Required Python Packages
Make sure you install the following Python packages:

Flask

python-dotenv

google-generativeai

You can install them using pip (Python's package installer).

🤖 Tech Stack
Flask (Python web framework)

Gemini AI (Google Generative AI)

HTML/CSS/JS (Frontend UI)

Mock Data (for events and customers)