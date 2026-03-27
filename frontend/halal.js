const API="https://stockpulsebadhoneditzx.up.railway.app";

function checkHalal(){
  console.log("Clicked");

  const symbol = document.getElementById("symbol").value.trim().toUpperCase();

  if(!symbol){
    alert("Enter symbol");
    return;
  }

  const result = document.getElementById("result");
  const info = document.getElementById("info");

  result.innerText = "Checking...";
  result.className = "result unknown";

  fetch(API + "/halal/" + symbol)
  .then(res => res.json())
  .then(data => {

    console.log(data);

    const status = data.status;

    result.innerText = status;

    if(status === "HALAL"){
      result.className = "result halal";
      info.innerHTML = "✅ Halal compliant stock";
    }

    else if(status === "HARAM"){
      result.className = "result haram";
      info.innerHTML = "❌ Not halal (financial sector)";
    }

    else{
      result.className = "result unknown";
      info.innerHTML = "⚠️ Unknown";
    }

  })
  .catch(err => {
    console.error(err);
    result.innerText = "ERROR";
  });
}
