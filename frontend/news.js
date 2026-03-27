const API = "https://stockpulsebadhoneditzx.up.railway.app";

function loadNews(){
  fetch(API + "/news")
  .then(res => res.json())
  .then(data => {

    const container = document.getElementById("news");
    if(!container) return;

    container.innerHTML = "";

    if(!data || data.length === 0){
      container.innerHTML = "<p>No news available</p>";
      return;
    }

    let html = "";

    data.forEach(n => {

      // 🔥 sentiment color
      let sentimentColor = "#94a3b8";
      if(n.sentiment === "Bullish") sentimentColor = "#22c55e";
      if(n.sentiment === "Bearish") sentimentColor = "#ef4444";

      // 🔥 safe values
      let title = n.title || "No title";
      let summary = (n.summary || "").substring(0,120);
      let image = n.image || "https://picsum.photos/400/200";
      let url = n.url || "#";

      html += `
        <div class="news-card" onclick="window.open('${url}')">

          <img src="${image}" class="news-img">

          <div class="news-content">

            <div class="news-title">${title}</div>

            <div class="news-summary">
              ${summary}...
            </div>

            <div class="news-extra">
              ⚡ ${n.effect || "Market impact expected"}
            </div>

            <div class="news-extra">
              📊 Sector: ${n.sector || "General"}
            </div>

            <div class="news-extra" style="color:${sentimentColor};">
              🧠 ${n.sentiment || "Neutral"}
            </div>

          </div>

        </div>
      `;
    });

    container.innerHTML = html;

  })
  .catch(err => {
    console.log("News error:", err);
  });
}

// 🔁 auto reload (optional pro feature)
setInterval(loadNews, 60000);

// INIT
loadNews();
