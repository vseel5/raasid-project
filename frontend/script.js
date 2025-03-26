const BASE_URL = "http://127.0.0.1:8000";
console.log("Raasid frontend JS loaded");


function checkStatus() {
  const statusElement = document.getElementById("api-status");
  statusElement.innerText = "Checking...";  // <-- This should appear first!

  fetch(`${BASE_URL}/`)
    .then(res => res.json())
    .then(data => {
      statusElement.innerText = data.message;
    })
    .catch(() => {
      statusElement.innerText = "Error connecting to API";
    });
}


function loadLogs() {
  const logOutput = document.getElementById("log-output");
  logOutput.innerText = "Loading...";

  fetch(`${BASE_URL}/decision_logs`)
    .then(res => res.json())
    .then(data => {
      logOutput.innerText = JSON.stringify(data, null, 2);
    })
    .catch(() => {
      logOutput.innerText = "Error loading logs.";
    });
}

function submitOverride() {
  const frame = parseInt(document.getElementById("frame").value);
  const override = document.getElementById("override").value.trim();
  const status = document.getElementById("override-status");

  if (!frame || !override) {
    status.innerText = "Please enter both frame number and override decision.";
    return;
  }

  status.innerText = "Submitting...";

  fetch(`${BASE_URL}/var_review`, {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ frame: frame, override_decision: override })
  })
    .then(res => res.json())
    .then(data => {
      status.innerText = data.message;
    })
    .catch(() => {
      status.innerText = "Error submitting override.";
    });
}

function distribute() {
  const outputStatus = document.getElementById("output-status");
  outputStatus.innerText = "Distributing...";

  fetch(`${BASE_URL}/output_distribution`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      outputStatus.innerText = data.message;
    })
    .catch(() => {
      outputStatus.innerText = "Error distributing decision.";
    });
}

function renderTimeline() {
  const timelineContainer = document.getElementById("timeline-container");
  timelineContainer.innerHTML = "Loading...";

  fetch(`${BASE_URL}/decision_logs`)
    .then(res => res.json())
    .then(data => {
      if (data.length === 0) {
        timelineContainer.innerHTML = "<p>No decisions yet</p>";
        return;
      }

      timelineContainer.innerHTML = ""; // Clear previous entries

      data.slice().reverse().forEach(entry => {
        const div = document.createElement("div");
        div.classList.add("timeline-entry");

        const score = entry.certainty_score;
        const isVAR = entry.VAR_review;
        let statusClass = "";

        if (score >= 95 && !isVAR) {
          statusClass = "entry-accepted";
        } else if (isVAR) {
          statusClass = "entry-var";
        } else {
          statusClass = "entry-error";
        }

        div.classList.add(statusClass);

        div.innerHTML = `
          <strong>Frame:</strong> ${entry.frame} <br>
          <strong>Decision:</strong> ${entry.final_decision} <br>
          <strong>Certainty:</strong> ${entry.certainty_score}% <br>
          <strong>VAR Review:</strong> ${entry.VAR_review ? "Yes" : "No"}
        `;

        timelineContainer.appendChild(div);
      });
    })
    .catch(() => {
      timelineContainer.innerHTML = "<p>Error loading timeline.</p>";
    });
}

setInterval(renderTimeline, 30000); // Refresh every 30 seconds


window.onload = () => {
  renderTimeline();
};

