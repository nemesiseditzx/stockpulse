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

    // 🔥 ADD THESE 2 LINES
    renderStocks(data);
    renderTopMovers(data);
    renderSummary(data);

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

// ================= GLOBAL ALERT POPUP =================

const ALERT_API = "https://stockpulsebadhoneditzx.up.railway.app";

let lastAlertTime = localStorage.getItem("lastAlertTime") || 0;
const sound = new Audio("ding.mp3");

function checkAlerts(){

  fetch(ALERT_API + "/alerts-today")
  .then(res => res.json())
  .then(data => {

    if(!data || !data.length) return;

    const latest = data[0];

    if(Number(latest.time) > Number(lastAlertTime)){

      showPopup(latest);
      playSound();

      localStorage.setItem("lastAlertTime", latest.time);
      lastAlertTime = latest.time;
    }

  })
  .catch(()=>{});
}


// 🔥 POPUP
function showPopup(alert){

  const div = document.createElement("div");

  div.style.position = "fixed";
  div.style.top = "20px";
  div.style.right = "20px";
  div.style.background = "#020617";
  div.style.color = "white";
  div.style.padding = "12px";
  div.style.borderRadius = "10px";
  div.style.boxShadow = "0 0 15px #3b82f6";
  div.style.zIndex = "9999";

  div.innerHTML = `
    <strong>🚨 New Alert</strong><br>
    ${alert.text || ""}
  `;

  document.body.appendChild(div);

  setTimeout(() => div.remove(), 4000);
}


// 🔊 SOUND
function playSound(){
  sound.currentTime = 0;
  sound.play().catch(()=>{});
}


// AUTO RUN
setInterval(checkAlerts, 5000);
