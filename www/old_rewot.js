var speed = 1;
var line_num = 1;

function ready_to_play() {
  var el = document.getElementById("ready_to_play");
  el.style.visibility = "visible";
}

function read_log() {
  var frame = document.getElementById("log");
  var log = frame.contentWindow.document.body.childNodes[0].textContent;
  var lines = log.split("\n");

  var out = document.getElementById("out");
  out.innerHTML += "<p style='color: yellow'>Playing log</p>";
  print_lines(lines, out, null);
}

function print_lines(lines, el, line) {
  // This function is called repeatedly, once for each line in the log output.
  // If the "last_ts" value is greater than or equal to the timestamp in the
  // log message, we display the line now. Otherwise, we schedule it for later.
  if(line != null) {
    el.innerHTML += line + "\n";
    window.scrollTo(0, document.body.scrollHeight);
  }
  
  if(lines.length === 0 || !lines) {
    el.innerHTML += "<p style='color: yellow'>Log complete</p>";
    window.scrollTo(0, document.body.scrollHeight);
    return;
  }
  
  var el_num = document.getElementById("line_num");
  el_num.innerHTML = line_num;

  var re = new RegExp(/^(\d+(?:\.\d+)?)(?: (.*))?$/);
  
  line = lines[0];

  //console.log("Processing line", line);

  var m = line.match(re);
  if(!m) {
    console.error('Cannot match line', line);
    return print_lines(lines.slice(1), el, null);
  }

  //console.log('  Got matches', m);

  var delta = parseFloat(m[1]);
  var output = "";
  if (m[2]) {
    output = m[2];
  }

  //console.log('  Line delta', delta);
  
  
  lines = lines.slice(1);
  
  line_num++;
  
  var el_delta = document.getElementById("delta");
  el_delta.innerHTML = delta * speed;
  
  setTimeout(function() {
    print_lines(lines, el, output);
  }, delta * speed * 1000);
}

function speed_up() {
  speed /= 2;
  var el_speed = document.getElementById("speed");
  el_speed.innerHTML = 1 / speed;
}

function slow_down() {
  speed *= 2;
  var el_speed = document.getElementById("speed");
  el_speed.innerHTML = 1 / speed;
}
