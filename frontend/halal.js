const API="https://stockpulsebadhoneditzx.up.railway.app";

function checkHalal(){
  const symbol = document.getElementById("symbol").value;

  fetch(API + "/halal/" + symbol)
  .then(res => res.json())
  .then(data => {
    const result = document.getElementById("result");

    result.innerText = data.status + " (Powered by Badhon EditZX)";

    if(data.status==="HALAL") result.style.color="green";
    else if(data.status==="HARAM") result.style.color="red";
    else result.style.color="gray";
  });
}
