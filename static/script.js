document.addEventListener("DOMContentLoaded", () => {
  fetchEvents();
});

// Fetch and display mock events
function fetchEvents() {
  fetch("/api/events")
    .then(response => response.json())
    .then(data => {
      const trendingContainer = document.getElementById("trending-events");
      trendingContainer.innerHTML = "";

      data.forEach(event => {
        const eventCard = document.createElement("div");
        eventCard.className = "event-card";

        eventCard.innerHTML = `
          <h3>${event.title}</h3>
          <p><strong>Location:</strong> ${event.location}</p>
          <p><strong>Date:</strong> ${event.date}</p>
          <div class="badges">
            ${event.genres.map(genre => `<span class="badge genre">${genre}</span>`).join('')}
            ${event.artists.map(artist => `<span class="badge artist">${artist}</span>`).join('')}
          </div>
          <button class="insight-button" data-id="${event.id}">Vibe Check</button>
          <div class="insight-output" id="insight-${event.id}"></div>
        `;

        trendingContainer.appendChild(eventCard);
      });

      setupInsightButtons();
    });
}

// Handle Gemini insight requests
function setupInsightButtons() {
  const buttons = document.querySelectorAll(".insight-button");
  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const eventId = button.getAttribute("data-id");
      const insightBox = document.getElementById(`insight-${eventId}`);
      insightBox.innerHTML = "Loading insight...";

      fetch(`/api/event_insight/${eventId}`)
        .then(response => response.json())
        .then(data => {
          insightBox.innerHTML = `
            <div class="insight-text">${data.insight}</div>
          `;
        })
        .catch(err => {
          insightBox.innerHTML = "Error fetching insight.";
        });
    });
  });
}
