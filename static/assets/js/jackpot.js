
var v = new Array();
var vDisp = new Array();
var jpCount = 0;
var jackpotTimer;
var secondToReload = 110;
var msecToBlink = 110;
var msecLoaded = 0;

function increaseJackpot() {
    for (i = 0; i < jpCount; i++) {
        if (isNaN(vDisp[i])) {

        }
        else {
            vDisp[i] += 0.001;
        }

        displayJackpotValues("pt_" + i, vDisp[i]);
    }
}
function getRandomInt(min, max) {
						    num =(Math.random() * (min - max) + max).toFixed(2)
						    return num
						}
function addCommas(nStr)
						{
						    nStr += '';
						    x = nStr.split('.');
						    x1 = x[0];
						    x2 = x.length > 1 ? '.' + x[1] : '';
						    var rgx = /(\d+)(\d{3})/;
						    while (rgx.test(x1)) {
						        x1 = x1.replace(rgx, '$1' + ',' + '$2');
						    }
						    return x1 + x2;
						}
function getJackpotValues(myValues, jpCountValue) {
    jpCount = jpCountValue;

    var d = new Date();
    var year = d.getFullYear().toString().length == 1 ? "0" + d.getFullYear().toString() : d.getFullYear().toString();
    var month = d.getMonth().toString().length == 1 ? "0" + d.getMonth().toString() : d.getMonth().toString();
    var date = d.getDate().toString().length == 1 ? "0" + d.getDate().toString() : d.getDate().toString();
    var hour = d.getHours().toString().length == 1 ? "0" + d.getHours().toString() : d.getHours().toString();
    var min = d.getMinutes().toString().length == 1 ? "0" + d.getMinutes().toString() : d.getMinutes().toString();
    var dateOffset = month + date + hour + min;

    for (i = 0; i < jpCount; i++) {
        if (isNaN(myValues.split(";")[i])) {
            vDisp[i] = myValues.split(";")[i];
        }
        else {
        	//getRandomInt(100000.00, 200000.99)
            v[i] = parseInt(myValues.split(";")[i]) + parseInt(dateOffset*300);
            vDisp[i] = v[i];
        }
    }

    if (msecLoaded == 0) jackpotTimer = window.setTimeout(increaseJackpot, msecToBlink);
}

function displayJackpotValues(myID, myVal) {

    msecLoaded += msecToBlink

    if (isNaN(myVal)) {
        document.getElementById(myID).innerHTML = myVal;
    }
    else {
        document.getElementById(myID).innerHTML = parseFloat(myVal).formatMoney(3, ',', '.');
    }

    if ((secondToReload * 1000) <= msecLoaded) {
        msecLoaded = 1;
        window.clearTimeout(jackpotTimer);
        //loadJackpot();
        jackpotTimer = window.setTimeout(increaseJackpot, msecToBlink);
    }
    else {
        window.clearTimeout(jackpotTimer);
        jackpotTimer = window.setTimeout(increaseJackpot, msecToBlink);
    }
}

Number.prototype.formatMoney = function (decPlaces, thouSeparator, decSeparator) {
    var n = this,
        decPlaces = isNaN(decPlaces = Math.abs(decPlaces)) ? 2 : decPlaces,
        decSeparator = decSeparator == undefined ? "." : decSeparator,
        thouSeparator = thouSeparator == undefined ? "," : thouSeparator,
        sign = n < 0 ? "-" : "",
        i = parseInt(n = Math.abs(+n || 0).toFixed(decPlaces)) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return sign + (j ? i.substr(0, j) + thouSeparator : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thouSeparator) + (decPlaces ? decSeparator + Math.abs(n - i).toFixed(decPlaces).slice(2) : "100");
};





// variables
var topPosition = $('.floating-div').offset().top - 10;
var floatingDivHeight = $('.floating-div').outerHeight();
var footerFromTop = $('footer').offset().top;
var absPosition = footerFromTop - floatingDivHeight - 20;
var win = $(window);
var floatingDiv = $('.floating-div');

win.scroll(function() {
  if (window.matchMedia('(min-width: 768px)').matches) {
    if ((win.scrollTop() > topPosition) && (win.scrollTop() < absPosition)) {
      floatingDiv.addClass('sticky');
      floatingDiv.removeClass('abs');

    } else if ((win.scrollTop() > topPosition) && (win.scrollTop() > absPosition)) {
      floatingDiv.removeClass('sticky');
      floatingDiv.addClass('abs');

    } else {
      floatingDiv.removeClass('sticky');
      floatingDiv.removeClass('abs');
    }
  }
});
