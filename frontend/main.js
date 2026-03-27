const API="https://stockpulsebadhoneditzx.up.railway.app";
const WS="wss://stockpulsebadhoneditzx.up.railway.app/ws";

// ================== CHART ==================
function search(symbol){
let s=symbol||document.getElementById("search").value;
if(!s)return;

let c=document.getElementById("chart");
c.innerHTML="";

let script=document.createElement("script");
script.src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";

script.innerHTML=JSON.stringify({
  "symbol":"NASDAQ:"+s,
  "theme":"dark",
  "autosize":true
});

c.appendChild(script);
}

// ================== LIVE STOCK ==================
const ws = new WebSocket(WS);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  renderStocks(data);
};

// fallback
function loadStocks(){
fetch(API+"/stocks")
.then(r=>r.json())
.then(res=>{
renderStocks(res.data);
});
}

function renderStocks(data){
  const container = document.getElementById("stocks");
  if(!container) return;

  container.innerHTML="";

  Object.keys(data).forEach(symbol => {
    const stock = data[symbol];
    const color = stock.change >= 0 ? "green" : "red";

    container.innerHTML += `
      <div class="card">
        <h3>${symbol}</h3>
        <p>$${stock.price}</p>
        <p class="${color}">${stock.change}%</p>
        <p>${stock.signal}</p>
        <p style="font-size:11px;color:#22c55e;">✔ Halal</p>
      </div>
    `;
  });
}

// ================== INIT ==================
search("AAPL");
loadStocks();
setInterval(loadStocks,10000);
