var x = document.getElementsByClassName("messages");

var y = document.getElementsByTagName("li");

if (y[0].className == "error"){
  x[0].style.backgroundColor = "red";
}

else if (y[0].className == "success"){
  x[0].style.backgroundColor = "green";
}

else if (y[0].className == "info"){
  x[0].style.backgroundColor = "blue";
}

setTimeout(function(){x[0].style.visibility = "hidden";}, 3000);
