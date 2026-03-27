const API="https://stockpulsebadhoneditzx.up.railway.app";

function loadSignals(){
  fetch(API + "/signals-live")
  .then(res => res.json())
  .then(data => {

    const feed = document.getElementById("feed");
    feed.innerHTML="";

    data.forEach(msg => {

      const div = document.createElement("div");
      div.className="msg";

      div.innerHTML = `
        <div class="time">📢 Live Update</div>
        <div class="text">${format(msg.text)}</div>
      `;

      feed.appendChild(div);

    });

  });
}

function format(text){
  if(!text) return "";

  // highlight BUY / SELL
  text = text.replace(/BUY/gi, "<span style='color:#22c55e'>BUY</span>");
  text = text.replace(/SELL/gi, "<span style='color:#ef4444'>SELL</span>");

  return text;
}

// 🔁 auto refresh
loadSignals();
setInterval(loadSignals, 5000);
