const API = "https://stockpulsebadhoneditzx.up.railway.app";

function loadAlerts(){

  fetch(API + "/alerts-today")
  .then(res => res.json())
  .then(data => render("today", data))
  .catch(err => console.log("ERROR:", err));

  fetch(API + "/alerts-previous")
  .then(res => res.json())
  .then(data => render("previous", data))
  .catch(err => console.log("ERROR:", err));

}


function render(id, data){
  const container = document.getElementById(id);
  container.innerHTML = "";

  if(!data || data.length === 0){
    container.innerHTML = "<p style='color:#94a3b8;'>No alerts</p>";
    return;
  }

  data.forEach(a => {

    const d = new Date(a.time * 1000);
    const time = d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    const date = d.toLocaleDateString();

    container.innerHTML += `
      <div class="card">

        ${a.image ? `<img src="${a.image}">` : ""}

        <div style="font-size:12px;color:#94a3b8;">
          🕒 ${date} • ${time}
        </div>

        <div style="margin-top:6px;">
          ${a.text || ""}
        </div>

      </div>
    `;
  });
}


// INIT
loadAlerts();
setInterval(loadAlerts, 5000);
