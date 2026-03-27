const API = "https://stockpulsebadhoneditzx.up.railway.app";

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
    "autosize": true
  });

  c.appendChild(script);
}

// ================== LOAD STOCKS ==================
function loadStocks(){
  fetch(API + "/stocks")
  .then(r => r.json())
  .then(res => {

    let data = res.data || res;

    renderStocks(data);

  })
  .catch(() => {
    console.log("API error");
  });
}

// ================== RENDER ==================
function renderStocks(data){
  let c = document.getElementById("stocks");
  if(!c) return;

  c.innerHTML = "";

  Object.keys(data).forEach(symbol => {
    let i = data[symbol];

    let color = i.change >= 0 ? "green" : "red";
    let arrow = i.change >= 0 ? "▲" : "▼";

    c.innerHTML += `
      <div class="card">
        <h3>${symbol}</h3>

        <p style="font-size:18px;font-weight:bold;">
          $${i.price}
        </p>

        <p class="${color}">
          ${arrow} ${i.change}%
        </p>

        <p style="margin-top:6px;">
          ${i.signal}
        </p>

        <p style="font-size:11px;color:#22c55e;">
          ✔ Halal
        </p>
      </div>
    `;
  });
}

// ================== TOP MOVERS ==================
function renderTopMovers(data){

  let arr = Object.keys(data).map(s => ({
    symbol: s,
    ...data[s]
  }));

  // sort by change
  let gainers = [...arr].sort((a,b)=>b.change-a.change).slice(0,5);
  let losers = [...arr].sort((a,b)=>a.change-b.change).slice(0,5);

  renderMini("gainers", gainers);
  renderMini("losers", losers);
}

function renderMini(id, list){
  let c = document.getElementById(id);
  if(!c) return;

  c.innerHTML="";

  list.forEach(i=>{
    let color = i.change>=0?"green":"red";
    let arrow = i.change>=0?"▲":"▼";

    c.innerHTML += `
      <div class="card">
        <h3>${i.symbol}</h3>
        <p>$${i.price}</p>
        <p class="${color}">
          ${arrow} ${i.change}%
        </p>
      </div>
    `;
  });
}

// ================== SUMMARY ==================
function renderSummary(data){
  let total = Object.keys(data).length;
  let gain = 0;
  let loss = 0;

  Object.values(data).forEach(i=>{
    if(i.change>=0) gain++;
    else loss++;
  });

  document.getElementById("summary").innerHTML = `
    <div>📊 Total: ${total}</div>
    <div class="green">📈 Gainers: ${gain}</div>
    <div class="red">📉 Losers: ${loss}</div>
  `;
}

// ================== INIT ==================
search("AAPL");
loadStocks();
setInterval(loadStocks, 10000);
