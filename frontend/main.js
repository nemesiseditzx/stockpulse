const API = "https://stockpulsebadhoneditzx.up.railway.app";
const WS = "wss://stockpulsebadhoneditzx.up.railway.app/ws";

// ================== CHART ==================
function search(symbol){
  let s = symbol || document.getElementById("search").value;
  if(!s) return;

  let c = document.getElementById("chart");
  c.innerHTML = "";

  let script = document.createElement("script");
  script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";

  script.innerHTML = JSON.stringify({
    "symbol": "NASDAQ:" + s,
    "theme": "dark",
    "autosize": true,
    "hide_top_toolbar": false,
    "hide_legend": false
  });

  c.appendChild(script);
}

// ================== WEBSOCKET ==================
let ws;

function connectWS(){
  ws = new WebSocket(WS);

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    renderStocks(data);
  };

  ws.onclose = () => {
    console.log("WS disconnected, retrying...");
    setTimeout(connectWS, 3000); // 🔁 auto reconnect
  };

  ws.onerror = () => {
    ws.close();
  };
}

// ================== FETCH FALLBACK ==================
function loadStocks(){
  fetch(API + "/stocks")
  .then(r => r.json())
  .then(res => {
    renderStocks(res.data); // ✅ IMPORTANT FIX
  })
  .catch(() => {
    console.log("API error");
  });
}

// ================== RENDER ==================
function renderStocks(data){
  const container = document.getElementById("stocks");
  if(!container) return;

  container.innerHTML = "";

  Object.keys(data).forEach(symbol => {
    const stock = data[symbol];

    const color = stock.change >= 0 ? "green" : "red";
    const arrow = stock.change >= 0 ? "▲" : "▼";

    container.innerHTML += `
      <div class="card">
        <h3>${symbol}</h3>
        <p>$${stock.price}</p>
        <p class="${color}">
          ${arrow} ${stock.change}%
        </p>
        <p><b>${stock.signal}</b></p>
        <p style="font-size:11px;color:#22c55e;">
          ✔ Halal
        </p>
      </div>
    `;
  });
}

// ================== INIT ==================
search("AAPL");

// 🔥 connect websocket first
connectWS();

// 🔁 fallback refresh
loadStocks();
setInterval(loadStocks, 10000);

alert("NEW JS LOADED");
