function header() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}
var count = 0;
function sipcall() {
  if (count == 0) {
    document.getElementById("stepsip").style.display = "block";
    count++;
  }
  else {
    document.getElementById("stepsip").style.display = "none";
    count--;
  }
}

$(document).ready(function () {
  $('#load_data').click(function () {
      $.ajax({
          url: "static/cardata.csv",
          dataType: "text",
          success: function (data) {
              var employee_data = data.split(/\r?\n|\r/);
              var table_data = '<table class="table table-bordered table-striped">';
              for (var count = 0; count < employee_data.length; count++) {
                  var cell_data = employee_data[count].split(",");
                  table_data += '<tr>';
                  for (var cell_count = 0; cell_count < cell_data.length; cell_count++) {
                      if (count === 0) {
                          table_data += '<th>' + cell_data[cell_count] + '</th>';
                      }
                      else {
                          table_data += '<td>' + cell_data[cell_count] + '</td>';
                      }
                  }
                  table_data += '</tr>';
              }
              table_data += '</table>';
              $('#data_table').html(table_data);
          }
      });
  });

});

function plan() {
  if (!document.detail.goalamount.value == "" && !document.detail.invamount.value == "")
    document.getElementById("result").style.display = "block";

  var gamt = document.getElementById("goalamount").value;
  var iamt = parseFloat(document.getElementById("invamount").value);
  var roi = [3.5, 5.5, 8, 16, 9, 12, 8, 8];

  if (document.getElementById("type").value == "One-Time")
    for (var i = 0; i < 8; i++) {
      var y = (Math.log(gamt / iamt) / Math.log(1 + roi[i] / 100));
      var m = ((y - Math.floor(y)) * 12).toFixed(0);
      y = Math.floor(y);

      var goal = document.getElementById(i + 1 + "G");
      goal.textContent = "Goal Amount : " + gamt.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

      var res1 = document.getElementById(i + 1 + "A");
      res1.textContent = "Total Amount invested : " + (iamt).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

      var res2 = document.getElementById(i + 1 + "B");
      res2.textContent = "Earned Interest : " + (gamt - iamt).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

      var res3 = document.getElementById(i + 1 + "C");
      res3.textContent = "Time taken :" + y + " years  and " + m + "months";
    }

  if (document.getElementById("type").value == "Sip")
    for (var i = 0; i < 8; i++) {
      var r = roi[i] / 1200;

      var m = Math.ceil(Math.log((gamt * r / iamt / (1 + r)) + 1) / Math.log(1 + r));
      var y = Math.floor(m / 12);
      m = m % 12;
      var goal = document.getElementById(i + 1 + "G");
      goal.textContent = "Goal Amount : " + gamt.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

      var res1 = document.getElementById(i + 1 + "A");
      res1.textContent = "Total Amount invested : " + (iamt * (12 * y + m)).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

      var res2 = document.getElementById(i + 1 + "B");
      res2.textContent = "Earned Interest : " + (gamt - iamt * (12 * y + m)).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

      var res3 = document.getElementById(i + 1 + "C");
      res3.textContent = "Time taken :" + y + " years  and " + m + "months";
    }

  if (document.getElementById("type").value == "Step-Sip")
    for (var i = 0; i < 8; i++) {
      var r = roi[i] / 1200;
      var a = 0;
      var count = 0;
      var m = 0;
      var siprate = document.getElementById("sip%").value;
      var iamttemp = iamt;
      var total = 0;
      while (a < gamt) {
        total = total + iamt;
        a = a * (1 + r) + iamttemp;
        count++;
        if (count == 12) {
          iamttemp = iamttemp * (1 + siprate / 100);
          count = 0;
        }

        m++;
      }
      var y = Math.floor((m / 12));
      m = m % 12;
      var goal = document.getElementById(i + 1 + "G");
      goal.textContent = "Goal Amount : " + gamt.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

      var res1 = document.getElementById(i + 1 + "A");
      res1.textContent = "Total Amount invested : " + total.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

      var res2 = document.getElementById(i + 1 + "B");
      res2.textContent = "Earned Interest : " + (gamt - total).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

      var res3 = document.getElementById(i + 1 + "C");
      res3.textContent = "Time taken :" + y + " years  and " + m + "months";
    }
}

function calculateloan() {
  if (!document.detail.loanamount.value == "" && !document.detail.tenure.value == "" && !document.detail.irate.value == "")
    document.getElementById("result").style.display = "block";

  var amt = document.getElementById("loanamount").value;
  var y = parseFloat(document.getElementById("tenure").value);
  var r = parseFloat(document.getElementById("irate").value);


  var goal = document.getElementById("eA");
  goal.textContent = "Loan Amount : " + amt.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

  var goal = document.getElementById("eB");
  goal.textContent = "Loan Tenure : " + y;
  y = Math.floor(y * 12);
  var goal = document.getElementById("eC");
  goal.textContent = "Interest Rate : " + r + "%";
  r = r / 1200;
  var install = (amt * r * ((1 + r) ** y) / (((1 + r) ** y) - 1)).toFixed(2);
  var goal = document.getElementById("eF");
  goal.textContent = "Total Amount paid : " + (install * y).toFixed(2).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
  var goal = document.getElementById("eD");
  goal.textContent = "Total Interest paid : " + (install * y - amt).toFixed(2).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

  var goal = document.getElementById("eE");
  goal.textContent = "Monthly Installment : " + install.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

}


function calculatesip() {
  if (!document.detail.sipamount.value == "" && !document.detail.tenure.value == "" && !document.detail.irate.value == "")
    document.getElementById("result").style.display = "block";

  var amt = document.getElementById("sipamount").value;
  var y = parseFloat(document.getElementById("tenure").value);
  var r = parseFloat(document.getElementById("irate").value);


  var goal = document.getElementById("eA");
  goal.textContent = "Monthly Installment: " + amt.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

  var goal = document.getElementById("eB");
  goal.textContent = "Investment Tenure : " + y;
  y = Math.floor(y * 12);
  var goal = document.getElementById("eC");
  goal.textContent = "Interest Rate : " + r + "%";
  r = r / 1200;

  var finalamt = (amt * ((1 + r) ** y - 1) * (1 + r) / r).toFixed(2);

  var goal = document.getElementById("eD");
  goal.textContent = "Total Interest earned : " + (finalamt - amt*y).toFixed(2).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

  var goal = document.getElementById("eE");
  goal.textContent = "Amount Accumulated : " + finalamt.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

}

function calculate() {
  if (!document.detail.amount.value == "" && !document.detail.cage.value == "" && !document.detail.rage.value == "")
    document.getElementById("result").style.display = "block";

  var amt = document.getElementById("amount").value;
  var cage = parseFloat(document.getElementById("cage").value);
  var rage = parseFloat(document.getElementById("rage").value);

  var goal = document.getElementById("eA");
  goal.textContent = "Current Monthly Expense : " + amt.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

  var goal = document.getElementById("eB");
  goal.textContent = "Current Age : " + cage;

  var goal = document.getElementById("eC");
  goal.textContent = "Retirement Age : " + rage;

  var exp = amt * (1 + 0.06) ** (rage - cage);

  var goal = document.getElementById("eD");
  goal.textContent = "Monthly Expense at age of " + rage + " at 6% inflation : " + (exp).toFixed(2).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

  var totalamt = 0;
  for (var i = rage; i <= 80; i++) {
    // console.log(exp);
    totalamt += exp * 12;
    exp = exp * 1.02;
  }
  var goal = document.getElementById("eE");
  goal.textContent = "Total money required from age " + rage + " till age of 80 :" + totalamt.toFixed(2).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
  r = 0.08 / 12;
  y = (rage - cage) * 12;
  var monthlyamt = (totalamt / (((1 + r) ** y - 1) * (1 + r) / r)).toFixed(2);
  var goal = document.getElementById("eF");
  goal.textContent = "Monthly investment required at avg(8%) interest till retirement and 4% after that : " + monthlyamt.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");



}
