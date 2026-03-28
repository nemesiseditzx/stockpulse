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

  data.forEach(a => {

    const time = new Date(a.time * 1000).toLocaleString();

    container.innerHTML += `
      <div class="card">

        ${a.image ? `<img src="${a.image}" style="width:100%;border-radius:8px;margin-bottom:10px;">` : ""}

        <p style="font-size:12px;color:#94a3b8;">
          ${time}
        </p>

        <p>${a.text}</p>

      </div>
    `;
  });
}

// auto refresh
loadAlerts();
setInterval(loadAlerts, 5000);
