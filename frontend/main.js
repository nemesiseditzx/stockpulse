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

// ================== INIT ==================
search("AAPL");
loadStocks();
setInterval(loadStocks, 10000);
