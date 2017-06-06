"use strict";

var counter = 1;
var elmain = document.getElementById("main");
var direction = "forward";
var fast_forward_lines = 0;
var json = null;
var lineno = 0;
var pausedid = null;
var playing = false;
var speed = 1;
var timeout = null;

function scroll(el) {
	var de = document.documentElement;
	
	if ((el.offsetTop < de.scrollTop) ||
			(el.offsetTop + el.offsetHeight > de.scrollTop + de.clientHeight)) {
		el.scrollIntoView();
	}
}

function add_line(line, visible) {
	var div = document.createElement("div");
	div.classList.add("replay-div");
	div.id = "replay-div-" + counter;
	div.innerHTML = line || "\n";
	elmain.appendChild(div);
	
	if (visible) {
		div.classList.add("replay-div-visible");
		scroll(div);
	}
	
	counter += 1;
	return counter - 1;
}

function notice(msg, now) {
	var s = '<div class="notice"><span>****</span> ' + msg;
	return add_line(s, now);
}

function del_line(id) {
	var el = document.getElementById("replay-div-" + id);
	if (el) {
		el.parentNode.removeChild(el);
	}
}

function finished() {
	playing = false;
	notice('Finished  <a href="/+' + json.meta.id + '">' +
		(json.meta.title || json.meta.id) + '</a>', true);
	document.getElementById("play_pause").className = "icon-play";
}

function forward() {
	direction = "forward";
	return false;
}

function xhr_load() {
	this.callback.apply(this, this.arguments);
}

function xhr_error() {
	console.error(this.statusText);
}

function fetch_json(url, callback) {
	var xhr = new XMLHttpRequest();
	xhr.callback = callback;
	xhr.onload = xhr_load;
	xhr.onerror = xhr_error;
	xhr.open("get", url, true);
	xhr.send(null);
}

function load_log_lines() {
	json = JSON.parse(this.responseText);
	
	if (!json) {
		notice("Loading failed", true);
		return;
	}
	
	var ready = notice((json.meta.title || json.meta.id) +
		' loaded  <a href="#" onclick="return play_pause();">Play</a>', false);
	
	json.log.forEach(function(line) {
		json.log[line.lineno - 1].lineid =
			add_line(line.line, false);
	});
	
	document.getElementById("progress").max = json.log.length;
	document.title = "ReWoT :: " + (json.meta.title || json.meta.id);
	document.getElementById("play_pause").className = "icon-play";
	update_progress();
	show_line(ready);
}

function load_log(url) {
	fetch_json(url, load_log_lines);
	return false;
}

function play_pause() {
	var el = document.getElementById("play_pause");
	
	if (playing) {
		if (timeout) {
			window.clearTimeout(timeout);
		}
		pausedid = notice("Paused", true);
		playing = false;
		document.getElementById("play_pause").className = "icon-play";
	} else {
		if (json) {
			playing = true;
			document.getElementById("play_pause").className = "icon-pause";
			if (pausedid) {
				del_line(pausedid);
			}
			if (lineno > json.log.slice(-1)[0].lineno) {
				lineno = json.log.slice(-1)[0].lineno;
			} else if (lineno < 1) {
				lineno = 1;
			}
			replay_log();
		} else {
			notice("No replay loaded", true);
		}
	}
	return false;
}

function replay_log() {
	if (!json.log[lineno] || !playing) {
		return;
	}
	
	show_line(json.log[lineno].lineid);
	
	if (direction == "forward") {
		lineno += 1;
	} else {
		hide_line(json.log[lineno].lineid);
		lineno -= 1;
	}
	
	if (json.log[lineno]) {
		if (fast_forward_lines) {
			fast_forward_lines -= 1;
			replay_log();
		} else {
			var d = parseFloat(json.log[lineno].delta) * speed;
			if (d > 4000) {
				d = 4000;
			}
			timeout = setTimeout(replay_log, d);
		}
		update_lineno();
		update_progress();
	} else {
		finished();
	}
}

function reverse() {
	direction = "reverse";
	return false;
}

function show_line(id) {
	var el = document.getElementById("replay-div-" + id);
	if (!!el) {
		el.classList.add("replay-div-visible");
		scroll(el);
	}
}

function hide_line(id) {
	var el = document.getElementById("replay-div-" + id);
	if (!!el) {
		el.classList.remove("replay-div-visible");
	}
}

function update_lineno() {
	document.getElementById("lineno").innerHTML = json.log[lineno].lineno;
}

function update_progress() {
	var el = document.getElementById("progress");
	el.value = json.log[lineno].lineno;
	el.title = json.log[lineno].lineno + " / " + el.max;
}

