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

// ================== STOCK ==================
const ws = new WebSocket(WS);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
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
      </div>
    `;
  });
};

// fallback
function loadStocks(){
fetch(API+"/stocks")
.then(r=>r.json())
.then(d=>{
let c=document.getElementById("stocks");
if(!c) return;

c.innerHTML="";

Object.keys(d).forEach(s=>{
let i=d[s];
let color=i.change>=0?"green":"red";

c.innerHTML+=`
<div class="card">
<h3>${s}</h3>
<p>$${i.price}</p>
<p class="${color}">${i.change}%</p>
<p>${i.signal}</p>
</div>
`;
});
});
}

search("AAPL");
loadStocks();
setInterval(loadStocks,10000);
