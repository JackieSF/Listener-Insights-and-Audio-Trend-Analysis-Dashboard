const eventList = document.getElementById("event-list");
const eventDetails = document.getElementById("event-details");
const audienceSection = document.getElementById("audience-section");

let inventory = [];

async function fetchEvents() {
  const res = await fetch("/inventory");
  const data = await res.json();
  inventory = data.inventory;
  renderEvents(inventory);
}

function renderEvents(events) {
  eventList.innerHTML = "";
  events.forEach(event => {
    const li = document.createElement("li");
    li.textContent = event.title;
    li.addEventListener("click", () => showEventDetails(event));
    eventList.appendChild(li);
  });
}

function showEventDetails(event) {
  audienceSection.innerHTML = "";

  eventDetails.innerHTML = `
    <h2>${event.title}</h2>
    <p><strong>Location:</strong> ${event.location}</p>
    <p><strong>Date:</strong> ${event.date}</p>
    <p><strong>Genres:</strong> ${event.genres.join(', ')}</p>
    <p><strong>Artists:</strong> ${event.artists.join(', ')}</p>
    <button onclick="getCuratedAudience('${event.id}')">Get Curated Audience</button>
  `;
}

async function getCuratedAudience(eventId) {
  const res = await fetch(`/curated-audience/${eventId}`);
  const data = await res.json();

  audienceSection.innerHTML = `<h3>Curated Audience</h3>`;
  data.audience.forEach(aud => {
    const div = document.createElement("div");
    div.className = "audience-card";
    div.innerHTML = `
      <p><strong>${aud.name}</strong> (${aud.location})</p>
      <p><em>Match Confidence: ${Math.round(aud.match_confidence * 100)}%</em></p>
      <p><strong>Top Genres:</strong> ${aud.top_genres.join(', ')}</p>
      <p><strong>Top Artists:</strong> ${aud.top_artists.join(', ')}</p>
      <p><strong>Recent Tracks:</strong> ${aud.recent_tracks.map(t => `"${t.name}" by ${t.artist}`).join(', ')}</p>
      <p style="margin-top: 10px;"><strong>Why this match?</strong> ${aud.match_reason}</p>
    `;
    audienceSection.appendChild(div);
  });
}

fetchEvents();
