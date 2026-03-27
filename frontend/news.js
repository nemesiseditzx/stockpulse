const API="https://stockpulsebadhoneditzx.up.railway.app";

function loadNews(){
  fetch(API + "/news")
  .then(res => res.json())
  .then(data => {

    const container = document.getElementById("news");
    container.innerHTML="";

    data.forEach(n => {

      container.innerHTML += `
        <div class="news-card" onclick="window.open('${n.url}')">
          <img src="${n.image || 'https://picsum.photos/400'}" class="news-img">

          <div class="news-content">
            <div class="news-title">${n.title}</div>
            <div class="news-summary">${(n.summary||"").substring(0,100)}...</div>
            <div style="font-size:12px;margin-top:8px;">
              ⚡ ${n.effect}
            </div>
            <div style="font-size:10px;color:gray;margin-top:6px;">
              Powered by Badhon EditZX
            </div>
          </div>
        </div>
      `;
    });

  });
}

loadNews();
