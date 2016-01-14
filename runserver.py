#!/usr/bin/env python3

import os

from rewot import app


# config settings for development
class Config:
	DEBUG = True


config = Config()

app.static_folder = os.path.join(os.getcwd(), "www")
app.config.from_object(config)
app.run()
