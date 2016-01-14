from os import getenv

from flask import Flask

app = Flask(__name__, static_url_path="")

# debug mode will be enabled if the environment variable REWOT_DEBUG=true,
# or if run via runserver.py
if getenv("REWOT_DEBUG"):
	if getenv("REWOT_DEBUG") == "true":
		from werkzeug.debug import DebuggedApplication
		app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
		app.config["DEBUG"] = True

import rewot.views
