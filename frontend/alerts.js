const API = "https://stockpulsebadhoneditzx.up.railway.app";

function loadAlerts(){

  // TODAY
  fetch(API + "/alerts-today")
  .then(res => res.json())
  .then(data => {
    render("today", data);
  });

  // PREVIOUS
  fetch(API + "/alerts-previous")
  .then(res => res.json())
  .then(data => {
    render("previous", data);
  });

}

function render(id, data){
  const container = document.getElementById(id);
  container.innerHTML = "";

  if(data.length === 0){
    container.innerHTML = "<p style='color:#94a3b8;'>No alerts yet</p>";
    return;
  }

  data.forEach(a => {

    const time = new Date(a.time * 1000).toLocaleString();

    container.innerHTML += `
      <div class="card">

        ${a.image ? `<img src="${a.image}">` : ""}

        <div class="time">🕒 ${time}</div>

        <div style="margin-top:6px;">
          ${formatText(a.text)}
        </div>

      </div>
    `;
  });
}
// auto refresh
loadAlerts();
setInterval(loadAlerts, 5000);
