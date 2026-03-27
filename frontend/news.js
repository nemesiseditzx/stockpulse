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

      card.onclick = () => {
        window.open(n.url, "_blank");
      };

      card.innerHTML = `
        <img src="${n.image || 'https://via.placeholder.com/400'}" class="news-img">

        <div class="news-content">

          <div class="news-source">${n.source}</div>

          <div class="news-title">${n.title}</div>

          <div class="news-summary">
            ${formatSummary(n.summary)}
          </div>

        </div>
      `;

      container.appendChild(card);

    });

  });
}

function formatSummary(text){
  if(!text) return "No summary available.";

  // make it look like "cause/effect"
  return "📌 " + text.substring(0,120) + "...";
}

loadNews();
