console.log('Hello from Node! :)');

var myfun1 = function(number, message) {
  console.log("Myfun1");
  var count = 0;
  while (count < number) {
    console.log(String(count) + ". " + message);
    count += 1;
  }
}

function myfun2(number, message) {
  console.log("Myfun2");
  var count = 0;
  while (count < number) {
    console.log(String(count) + ". " + message);
    count += 1;
  }
}

function myfun3() {
  console.log("Myfun 3");
}

function doTimes1(number, msgParam) {
  var count = 0;
  while (count < number) {
    // it is necessary to either wrap the "myfun1" call into an un-named "function(){}" to pass in parameters:
    setTimeout(function() { myfun1(number, msgParam); }, 100 + 2000*count);
    // or use "bind"
    setTimeout(myfun1.bind(null, number, msgParam), 100 + 2000*count);
    count += 1;
  }
}

function doTimes2(number, fun) {
  var count = 0;
  while (count < number) {
    setTimeout(fun, 100 + 2000*count);
    count += 1;
  }
}

doTimes1(3, "hi again");
doTimes2(3, myfun2.bind(null, 4, "number two"));
