from flask import Flask

app = Flask(__name__, static_url_path="")

import rewot.views
