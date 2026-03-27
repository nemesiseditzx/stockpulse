const API = "https://stockpulsebadhoneditzx.up.railway.app";

function loadAlerts(){
  console.log("Loading alerts...");

  fetch(API + "/alerts-live")
  .then(res => res.json())
  .then(data => {

    console.log("DATA:", data); // 🔥 DEBUG

    const container = document.getElementById("alerts");

    if(!container){
      console.log("❌ container not found");
      return;
    }

    container.innerHTML = "";

    if(!data || data.length === 0){
      container.innerHTML = "<p>No alerts yet...</p>";
      return;
    }

    data.forEach(a => {

      const time = new Date(a.time * 1000).toLocaleString();

      container.innerHTML += `
        <div class="card">

          ${a.image ? `<img src="${a.image}" style="width:100%;border-radius:8px;margin-bottom:10px;">` : ""}

          <p style="font-size:12px;color:#94a3b8;">
            ${time}
          </p>

          <p style="margin-top:6px;">
            ${formatText(a.text)}
          </p>

        </div>
      `;
    });

  })
  .catch(err => {
    console.log("❌ FETCH ERROR:", err);
  });
}

function formatText(text){
  if(!text) return "";

  text = text.replace(/BUY/gi, "<span style='color:#22c55e'>BUY</span>");
  text = text.replace(/SELL/gi, "<span style='color:#ef4444'>SELL</span>");

  return text;
}

// INIT
loadAlerts();
setInterval(loadAlerts, 5000);
