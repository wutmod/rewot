"use strict";




var elmain = document.getElementById("replay");
var fast_forward_lines = 0;
var id = window.location.pathname.slice(2);
var json = null;
var lineno = 0;
var playing = false;
var progress = 0;
var speed = 1;
var timeout = null;
var title = null;

function rewind() {
	if (playing) {
		window.clearTimeout(timeout);
	}
	
	var lines = elmain.innerHTML.split("\n");
	elmain.innerHTML = lines.slice(0, -15).join("\n");
	//window.scrollTo(0, document.body.scrollHeight);
	lineno -= 15;
	update_lineno();
	
	if (playing) {
		replay_log();
	}
	
	return false;
}

function fast_forward() {
	if (playing) {
		window.clearTimeout(timeout);
	}
	
	fast_forward_lines = 15;
	replay_log();
	
	return false;
}

function pause() {
	if (playing) {
		window.clearTimeout(timeout);
		elmain.innerHTML += '<p class="notice">Paused</p>\n';
		window.scrollTo(0, document.body.scrollHeight);
		playing = false;
	}
	return false;
}

function stop() {
	if (playing) {
		window.clearTimeout(timeout);
		playing = false;
	}
	elmain.innerHTML = '<p class="notice">Ready to play.</p>\n';
	window.scrollTo(0, document.body.scrollHeight);
	lineno = 0;
	update_lineno();
	return false;
}

function play() {
	playing = true;
	replay_log();
	return false;
}

function speed_up() {
	speed /= 2;
	document.getElementById("speed").innerHTML = 1 / speed;
	return false;
}

function slow_down() {
	speed *= 2;
	document.getElementById("speed").innerHTML = 1 / speed;
	return false;
}

function goto_line() {
	console.log("goto line");
	return false;
}

function update_lineno() {
	document.getElementById("lineno").innerHTML = json.log[lineno].lineno;
}

function replay_log() {
	if (!json.log[lineno] || (!playing && !fast_forward_lines)) {
		return;
	}
	
	update_lineno();
	
	if (json.log[lineno].show) {
		elmain.innerHTML += json.log[lineno].line + "\n";
		window.scrollTo(0, document.body.scrollHeight);
	}
	
	lineno += 1;
	
	if (json.log[lineno]) {
		if (fast_forward_lines) {
			fast_forward_lines -= 1;
			replay_log();
		} else {
			var d = json.log[lineno].delta * speed;
			if (d > 4000) {
				d = 4000;
			}
			timeout = setTimeout(replay_log, d);
		}
		
		for (var i = 1; i < 4; i++) {
			if (lineno + 1 >= json.log.length * i * .33) {
				document.getElementById("progress").className = "icon-progress-" + i;
			}
		}
	} else {
		playing = false;
		elmain.innerHTML += '<p class="notice">Finished</p>\n';
		window.scrollTo(0, document.body.scrollHeight);
	}
}

function ready_to_play() {
	if (json.meta.title) {
		title = json.meta.title;
	} else {
		title = json.meta.id;
	}
	
	document.title = "ReWoT :: " + title;
	elmain.innerHTML += '<p class="notice">Ready to play.</p>\n'
}

function get_json() {
	if (!id) {
		console.log("No ID")
		return;
	}
	
	var request = new XMLHttpRequest();
	request.open("GET", "/json/" + id + ".json", true);
	
	request.onload = function() {
		if (request.status >= 200 && request.status < 400) {
			json = JSON.parse(request.responseText);
			ready_to_play();
		} else {
			console.log("Failed to retrieve json from /json/" + id + ".json");
			console.log("Request status is " + request.status);
		}
	};
	
	request.onerror = function() {
		console.log("Failed to retrieve json from /json/" + id + ".json");
	};
	
	request.send();
};

get_json();
