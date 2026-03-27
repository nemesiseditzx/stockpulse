const API="https://stockpulsebadhoneditzx.up.railway.app";

function loadNews(){
  fetch(API + "/news")
  .then(res => res.json())
  .then(data => {

    const container = document.getElementById("news");
    container.innerHTML="";

    data.forEach(n => {

      const card = document.createElement("div");
      card.className="news-card";

      card.onclick = () => window.open(n.url, "_blank");

      card.innerHTML = `
        <img src="${n.image || 'https://picsum.photos/400'}" class="news-img">

        <div class="news-content">

          <div class="news-source">${n.source}</div>

          <div class="news-title">${n.title}</div>

          <div class="news-summary">
            ${short(n.summary)}
          </div>

          <div style="margin-top:10px;font-size:12px;">
            <b>⚡ Impact:</b> ${n.effect}
          </div>

        </div>
      `;

      container.appendChild(card);

    });

  });
}

function short(text){
  if(!text) return "No summary";
  return text.substring(0,100) + "...";
}

loadNews();
