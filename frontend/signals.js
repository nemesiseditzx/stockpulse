const API = "https://stockpulsebadhoneditzx.up.railway.app";

function loadSignals(){

  // CURRENT
  fetch(API + "/signals-current")
  .then(res => res.json())
  .then(data => {
    const feed = document.getElementById("current");
    feed.innerHTML = "";

    data.forEach(msg => {
      feed.appendChild(createMsg(msg));
    });
  });

  // PREVIOUS
  fetch(API + "/signals-previous")
  .then(res => res.json())
  .then(data => {
    const feed = document.getElementById("previous");
    feed.innerHTML = "";

    data.forEach(msg => {
      feed.appendChild(createMsg(msg, true));
    });
  });

}

function createMsg(msg, old=false){

  const div = document.createElement("div");
  div.className = "msg";

  const time = new Date(msg.time * 1000).toLocaleString();

  div.innerHTML = `
    <div class="time">${old ? "🕓 Previous" : "📢 Live"} • ${time}</div>
    <div class="text">${format(msg.text)}</div>
  `;

  return div;
}

function format(text){
  if(!text) return "";

  text = text.replace(/BUY/gi, "<span style='color:#22c55e'>BUY</span>");
  text = text.replace(/SELL/gi, "<span style='color:#ef4444'>SELL</span>");

  return text.replace(/\n/g, "<br>");
}

// AUTO REFRESH
loadSignals();
setInterval(loadSignals, 5000);
