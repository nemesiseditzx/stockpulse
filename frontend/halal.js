const API="https://stockpulsebadhoneditzx.up.railway.app";

function checkHalal(){
  const symbol = document.getElementById("symbol").value.trim().toUpperCase();

  if(!symbol) return;

  const result = document.getElementById("result");
  const info = document.getElementById("info");

  result.innerText = "Checking...";
  result.className = "result unknown";

  fetch(API + "/halal/" + symbol)
  .then(res => res.json())
  .then(data => {

    const status = data.status;

    result.innerText = status;

    if(status === "HALAL"){
      result.className = "result halal";
      info.innerHTML = "This stock appears compliant with halal investment principles.";
    }

    else if(status === "HARAM"){
      result.className = "result haram";
      info.innerHTML = "This stock is not halal due to involvement in prohibited sectors.";
    }

    else{
      result.className = "result unknown";
      info.innerHTML = "We could not determine the status. More data needed.";
    }

  })
  .catch(() => {
    result.innerText = "Error";
    result.className = "result unknown";
  });
}
