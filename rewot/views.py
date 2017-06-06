from flask import redirect, render_template, request

from rewot import app
import rewot.id
from rewot.log import Log


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/+<replayid>", methods=["GET"])
def replay(replayid):
	return render_template("replay.html", replayid=replayid)


@app.route("/submit", methods=["GET"])
def submit_page():
	return render_template("submit.html")


@app.route("/submit", methods=["POST"])
def submit_accept():
	""" Accept a new log submission. """
	
	form_log = request.form.get("submit_log", None)
	form_title = request.form.get("submit_title", None)
	form_player = request.form.get("submit_player", None)
	form_public = request.form.get("submit_public", None)
	
	log = Log(form_player, form_title)
	log.parse(form_log)
	
	print("meta: %s" % log.meta)
	print("title: %s" % form_title)
	print("player: %s" % form_player)
	print("public: %s" % form_public)
	print("log: %s" % form_log)
	
	if log.client == None:
		return render_template("error.html", error="Unknown client.")
	
	log.set_id(rewot.id.generate("www/json"))
	
	with open("www/json/{}.json".format(log.meta["id"]), "w") as f:
		f.write(log.get_json())
	with open("www/raw/{}.txt".format(log.meta["id"]), "w") as f:
		f.write(log.raw_log)
	
	return '<span class="notice">  ****  </span> {} <a href="/+{}" onclick="return load_log(\'/json/{}.json\');">Load</a><br>'.format(
		log.meta["title"], log.meta["id"], log.meta["id"], log.meta["title"])
