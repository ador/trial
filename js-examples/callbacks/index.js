console.log('Hello from Node! :)');

var myfun1 = function(number, message) {
  var count = 0;
  while (count < number) {
    console.log(String(count) + ". " + message);
    count += 1;
  }
}

var doTimes = function(number, func) {
  var count = 0;
  while (count < number) {
    func(2, "Hello");
    count += 1;
  }
}

doTimes(3, myfun1);
