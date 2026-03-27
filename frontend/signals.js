const API="https://stockpulsebadhoneditzx.up.railway.app";

function loadSignals(){

  fetch(API + "/signals-current")
  .then(res => res.json())
  .then(data => {
    const feed = document.getElementById("current");
    feed.innerHTML="";

    data.forEach(msg => {
      feed.appendChild(createMsg(msg));
    });
  });

  fetch(API + "/signals-previous")
  .then(res => res.json())
  .then(data => {
    const feed = document.getElementById("previous");
    feed.innerHTML="";

    data.forEach(msg => {
      feed.appendChild(createMsg(msg, true));
    });
  });
}

function createMsg(msg, old=false){

  const div = document.createElement("div");
  div.className="msg";

  const time = new Date(msg.time * 1000).toLocaleString();

  div.innerHTML = `
    <div class="time">${old ? "🕓 Previous" : "📢 Live"} • ${time}</div>
    <div class="text">${format(msg.text)}</div>
  `;

  return div;
}

// 🔥 FIXED FORMAT FUNCTION
function format(text){
  if(!text) return "";

  // line break fix
  text = text.replace(/\\n/g, "<br>");

  // remove markdown **
  text = text.replace(/\*\*/g, "");

  // BUY SELL highlight
  text = text.replace(/BUY/gi, "<span style='color:#22c55e;font-weight:bold'>BUY</span>");
  text = text.replace(/SELL/gi, "<span style='color:#ef4444;font-weight:bold'>SELL</span>");

  return text;
}

// auto refresh
loadSignals();
setInterval(loadSignals, 5000);
