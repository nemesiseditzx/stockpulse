const API = "https://stockpulsebadhoneditzx.up.railway.app";

function loadAlerts(){

  // TODAY
  fetch(API + "/alerts-today")
  .then(res => res.json())
  .then(data => render("today", data));

  // PREVIOUS
  fetch(API + "/alerts-previous")
  .then(res => res.json())
  .then(data => render("previous", data));

}


function render(id, data){
  const container = document.getElementById(id);
  container.innerHTML = "";

  if(data.length === 0){
    container.innerHTML = "<p style='color:#94a3b8;'>No alerts</p>";
    return;
  }

  data.forEach(a => {

    const d = new Date(a.time * 1000);

    const time = d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    const date = d.toLocaleDateString();

    const full = `${date} • ${time}`;

    container.innerHTML += `
      <div class="card">

        ${a.image ? `<img src="${a.image}">` : ""}

        <div class="time">🕒 ${full}</div>

        <div style="margin-top:6px;">
          ${formatText(a.text)}
        </div>

      </div>
    `;
  });
}


function formatText(text){
  if(!text) return "";

  text = text.replace(/BUY/gi, "<span style='color:#22c55e'>BUY</span>");
  text = text.replace(/SELL/gi, "<span style='color:#ef4444'>SELL</span>");

  return text;
}


// AUTO REFRESH
loadAlerts();
setInterval(loadAlerts, 5000);
