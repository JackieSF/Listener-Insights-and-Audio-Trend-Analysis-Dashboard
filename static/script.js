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
          <button class="toggle-button insight-button" data-id="${event.id}">
            <span class="arrow">►</span> Vibe Check
          </button>
          <div class="insight-output" id="insight-${event.id}" style="display: none;"></div>

          <button class="toggle-button curate-button" data-id="${event.id}">
            <span class="arrow">►</span> Curate Audience
          </button>
          <div class="audience-output" id="audience-${event.id}" style="display: none;"></div>
        `;

        trendingContainer.appendChild(eventCard);
      });

      // collapse insights 
document.querySelectorAll(".close-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    btn.parentElement.style.display = "none";
  });
});

      setupInsightButtons();
      setupCurateButtons(); 

    });
}

function setupCurateButtons() {
  const buttons = document.querySelectorAll(".curate-button");
  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const eventId = button.getAttribute("data-id");
      const audienceBox = document.getElementById(`audience-${eventId}`);
      const arrow = button.querySelector(".arrow");

      // Toggle visibility
      if (audienceBox.style.display === "none") {
        audienceBox.style.display = "block";
        arrow.textContent = "▼"; 
        audienceBox.innerHTML = "Finding potential audience...";

        fetch(`/api/curate_audience/${eventId}`)
          .then(response => response.json())
          .then(data => {
            const list = data.map(c => `<li>${c.name} - Likes ${c.top_genres.join(', ')}</li>`).join('');
            audienceBox.innerHTML = `<ul>${list}</ul>`;
          })
          .catch(() => {
            audienceBox.innerHTML = "Failed to curate audience.";
          });
      } else {
        audienceBox.style.display = "none";
        arrow.textContent = "►"; 
      }
    });
  });
}


// Handle Gemini insight requests
function setupInsightButtons() {
  const buttons = document.querySelectorAll(".insight-button");
  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const eventId = button.getAttribute("data-id");
      const insightBox = document.getElementById(`insight-${eventId}`);
      const arrow = button.querySelector(".arrow");

      // Toggle visibility
      if (insightBox.style.display === "none") {
        insightBox.style.display = "block";
        arrow.textContent = "▼";
        insightBox.innerHTML = "Loading insight...";

        fetch(`/api/event_insight/${eventId}`)
          .then(response => response.json())
          .then(data => {
            const insightText = data.insight;
            const sections = insightText.split(/\*\*(.*?)\*\*/); // Splits text by bolded sections

            let formatted = "<ul>";
            for (let i = 1; i < sections.length; i += 2) {
              let title = sections[i].trim().replace(/[:：]+$/, "");
              let body = sections[i + 1]?.trim().replace(/^\*|\*$/g, "").trim(); 

              if (body && body !== "*") {
                formatted += `<li><strong>${title}:</strong> ${body}</li>`;
              }
            }
            formatted += "</ul>";

            insightBox.innerHTML = `<div class="insight-text">${formatted}</div>`;

          })
          .catch(err => {
            insightBox.innerHTML = "Error fetching insight.";
          });
      } else {
        insightBox.style.display = "none";
        arrow.textContent = "►";
      }
    });
  });
}

