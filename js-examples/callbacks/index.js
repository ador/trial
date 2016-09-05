console.log('Hello from Node! :)');

var myfun1 = function(number, message) {
  var count = 0;
  while (count < number) {
    console.log(String(count) + ". " + message);
    count += 1;
  }
}

myfun1(3, "Hello")
