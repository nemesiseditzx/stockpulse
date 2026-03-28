const API = "https://stockpulsebadhoneditzx.up.railway.app";

let lastCount = 0;
const sound = new Audio("ding.mp3");

function loadAlerts(){

  fetch(API + "/alerts-today")
  .then(res => res.json())
  .then(data => {

    render("today", data);

    // 🔥 NEW ALERT DETECT
    if(data.length > lastCount){
      showPopup(data[0]);
      playSound();
    }

    lastCount = data.length;

  });

  fetch(API + "/alerts-previous")
  .then(res => res.json())
  .then(data => render("previous", data));

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
    const time = d.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
    const date = d.toLocaleDateString();

    container.innerHTML += `
      <div class="card">

        ${a.image ? `<img src="${a.image}" style="width:100%;border-radius:10px;">` : ""}

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


// 🔥 POPUP
function showPopup(alert){
  let popup = document.createElement("div");

  popup.style.position = "fixed";
  popup.style.bottom = "20px";
  popup.style.right = "20px";
  popup.style.background = "#1e293b";
  popup.style.padding = "12px";
  popup.style.borderRadius = "10px";
  popup.style.boxShadow = "0 0 10px #3b82f6";
  popup.style.zIndex = "9999";

  popup.innerHTML = `
    <strong>🚨 New Alert</strong><br>
    ${alert.text || ""}
  `;

  document.body.appendChild(popup);

  setTimeout(() => popup.remove(), 5000);
}


// 🔊 SOUND
function playSound(){
  sound.currentTime = 0;
  sound.play().catch(()=>{});
}


// INIT
loadAlerts();
setInterval(loadAlerts, 5000);
