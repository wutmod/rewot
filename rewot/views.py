from flask import redirect, render_template, request

from rewot import app
import rewot.id
from rewot.log import Log


@app.route("/submit", methods=["POST"])
def submit():
	""" Accept a new log submission. """
	
	form_log = request.form.get("log", None)
	form_title = request.form.get("title", None)
	form_player = request.form.get("player", None)
	
	log = Log(form_player, form_title)
	log.parse(form_log)
	log.set_id(rewot.id.generate("www/json"))
	
	with open("www/json/{}.json".format(log.meta["id"]), "w") as f:
		f.write(log.get_json())
	with open("www/raw/{}.txt".format(log.meta["id"]), "w") as f:
		f.write(log.raw_log)
	
	return "%s" % log.meta["id"]
