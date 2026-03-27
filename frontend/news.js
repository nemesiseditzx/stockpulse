const API="https://stockpulsebadhoneditzx.up.railway.app";

function loadNews(){
  fetch(API + "/news")
  .then(res => res.json())
  .then(data => {

    const container = document.getElementById("news");
    container.innerHTML="";

    data.forEach(n => {

      let sentimentColor = "#94a3b8";

      if(n.sentiment === "Bullish") sentimentColor = "#22c55e";
      if(n.sentiment === "Bearish") sentimentColor = "#ef4444";

      container.innerHTML += `
        <div class="news-card" onclick="window.open('${n.url}')">

          <img src="${n.image || 'https://picsum.photos/400'}" class="news-img">

          <div class="news-content">

            <div class="news-title">${n.title}</div>

            <div class="news-summary">
              ${(n.summary||"").substring(0,120)}...
            </div>

            <div style="margin-top:10px;font-size:13px;">
              ⚡ ${n.effect}
            </div>

            <div style="margin-top:5px;font-size:13px;">
              📊 Sector: ${n.sector}
            </div>

            <div style="margin-top:5px;font-size:13px;color:${sentimentColor};">
              🧠 ${n.sentiment}
            </div>

          </div>
        </div>
      `;
    });

  });
}

loadNews();
