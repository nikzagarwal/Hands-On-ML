function header() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}


count = 0;
function myFunction() {
  if (count == 0) {
    document.getElementById("classimodel").style.display = "none";
    document.getElementById("regmodel").style.display = "block";
    count++;
  }
  else {
    count--;
    document.getElementById("classimodel").style.display = "block";
    document.getElementById("regmodel").style.display = "none";
  }
  
}

function myFunction2(obj) {
  var value = obj.value;
  console.log(value);
  if (value =="naivebayes") {
    document.getElementById("n").style.display = "block";
    document.getElementById("k").style.display = "none";
    document.getElementById("d").style.display = "none";
    document.getElementById("dr").style.display = "none";
    document.getElementById("r").style.display = "none";

  }
  else if (value == "knn") {
    document.getElementById("n").style.display = "none";
    document.getElementById("k").style.display = "block";
    document.getElementById("d").style.display = "none";
    document.getElementById("dr").style.display = "none";
    document.getElementById("r").style.display = "none";
  }
  else if (value == "decisiontrees") {
    document.getElementById("n").style.display = "none";
    document.getElementById("k").style.display = "none";
    document.getElementById("d").style.display = "block";
    document.getElementById("dr").style.display = "block";
    document.getElementById("r").style.display = "none";
  }
  else if (value == "randomforest") {
    document.getElementById("n").style.display = "none";
    document.getElementById("k").style.display = "none";
    document.getElementById("d").style.display = "none";
    document.getElementById("dr").style.display = "block";
    document.getElementById("r").style.display = "block";
  }
}
 
function myFunction3(obj) {
  var value = obj.value;
  console.log(value);

  if (value == "linearreg") 
  {
    document.getElementById("n").style.display = "none";
    document.getElementById("k").style.display = "none";
    document.getElementById("d").style.display = "none";
    document.getElementById("dr").style.display = "none";
    document.getElementById("r").style.display = "none";
  }
  else if (value == "knnreg") {
    document.getElementById("n").style.display = "none";
    document.getElementById("k").style.display = "block";
    document.getElementById("d").style.display = "none";
    document.getElementById("dr").style.display = "none";
    document.getElementById("r").style.display = "none";
  }
  else if (value == "decisiontreereg") {
    document.getElementById("n").style.display = "none";
    document.getElementById("k").style.display = "none";
    document.getElementById("d").style.display = "block";
    document.getElementById("dr").style.display = "block";
    document.getElementById("r").style.display = "none";
  }
  else if (value == "randomforestreg") {
    document.getElementById("n").style.display = "none";
    document.getElementById("k").style.display = "none";
    document.getElementById("d").style.display = "none";
    document.getElementById("dr").style.display = "block";
    document.getElementById("r").style.display = "block";
  }
  
}
