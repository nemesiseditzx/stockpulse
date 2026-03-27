const API="https://stockpulsebadhoneditzx.up.railway.app";

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

function loadStocks(){
fetch(API+"/stocks")
.then(r=>r.json())
.then(res=>{

let data = res.data || res;

let c=document.getElementById("stocks");
c.innerHTML="";

Object.keys(data).forEach(s=>{
let i=data[s];

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
