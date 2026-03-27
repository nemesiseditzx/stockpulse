const API="https://stockpulsebadhoneditzx.up.railway.app";

function loadAlerts(){

  fetch(API + "/alerts-live")
  .then(res => res.json())
  .then(data => {

    const container = document.getElementById("alerts");
    if(!container) return;

    container.innerHTML = "";

    data.forEach(a => {

      const time = new Date(a.time * 1000).toLocaleTimeString();

      container.innerHTML += `
        <div class="alert-card">
          <div class="alert-time">⏱ ${time}</div>
          <div class="alert-text">${a.text}</div>
        </div>
      `;
    });

  });
}

// auto refresh
setInterval(loadAlerts, 5000);

loadAlerts();
