# -*- coding: utf-8 -*-
"""
	Log Object
	~~~~~~~~~~
	
	Log class, for parsing logs from the mud.
"""

import json
import re

from rewot.clients.tintin import TinTin
from rewot.clients.zmud import ZMud


class Log():
	"""
	This Log class is in charge of generating the JSON data based on the raw
	log. The actual parsing itself isn't generally done by this class but is
	handed off to specific helper classes. 
	"""
	
	def __init__(self, player=None, title=None):
		"""
		:param str title: Optional title of the log
		:param str player: Optional name of player
		"""
		
		self.meta = {
			"id": None,
			"title": None,
			"player": None
		}
		
		if player:
			self.meta["player"] = player
		
		if title:
			self.meta["title"] = title
		
		self.client = None
		self.log = []
		self.raw_log = None
	
	
	def _action(self, line):
		""" Perform an action based on a line from the log.
		
		:param str line: Line to parse as an action
		:return: Parsed action
		:rtype: dict
		
		Action lines begin with ``#!``, followed by the action, followed by a
		space (only required if there are aruments), then any arguments for the
		action. Example:
		
			``#!delay 1.8``
		
		In this way can certain features be provided to users to annotate the
		replay as they see fit.
		"""
		
		d = {}
		
		m = re.match(r"^#!(?P<action>\w+)(?: (?P<text>.*))?$", line)
		if m:
			action_match = m.groupdict().get("action")
			action_text = m.groupdict().get("text")
			
			if action_match == "client" and action_text:
				self._action_client(action_text)
			elif action_match == "delay" and action_text.isnumeric():
				d["delta"] = float(action_text)
				d["show"] = False
				d["text"] = ""
			elif action_match == "mark":
				d["delta"] = 0
				d["show"] = True
				d["text"] = '<hr class="action_mark">'
			elif action_match == "say" and action_text:
				d["delta"] = 0
				d["show"] = True
				d["text"] = '<p span="action_say">{}</p>'.format(action_text)
		return d
	
	
	def _action_client(self, client_string):
		""" Set the client type based on the ``#!client`` action found in the
		log.
		
		:param str client_string: The client string from the log
		"""
		
		if client_string.startswith("tintin"):
			last_client = self.client
			self.client = TinTin()
			if not self.client.set_client(client_string):
				self.client = last_client
		elif client_string.startswith("zmud"):
			last_client = self.client
			self.client = ZMud()
			if not self.client.set_client(client_string):
				self.client = last_client
	
	
	def _parse_line(self, line):
		""" Parse a line from the log with the appropriate client format.
		
		:param str line: Raw text of the line to parse
		:return: Parsed line
		:rtype: dict
		"""
		
		if self.client:
			return self.client.parse(line)
	
	
	def get_json(self):
		""" Return the JSON serialized dict containing the **meta** dict and
		the **log** list. This is a suitable format for the client side
		JavaScript to handle.
		
		:return: Parsed log in JSON format
		:rtype: str
		"""
		
		return json.dumps({"meta": self.meta, "log": self.log}, indent=4)
	
	
	def parse(self, raw_log):
		""" Read and parse the log. This is the main entry point for this class,
		and mostly delegates the work for each line to other functions or
		classes. Loops through every line in the log and delegates accordingly.
		
		:param str log: Raw text of the log to parse
		:return: Success
		:rtype: True or False
		"""
		
		if raw_log:
			self.raw_log = raw_log
			lineno = 1
			
			for line in raw_log.split("\n"):
				line_dict = {}
				line = line.rstrip("\r")
				
				if line.startswith("#!"):
					line_dict = self._action(line)
				elif line.startswith("##"):
					pass
				elif self.client:
					line_dict = self._parse_line(line)
				
				if line_dict:
					line_dict["lineno"] = lineno
					lineno += 1
					self.log.append(line_dict)
			return True
		else:
			return False
	
	
	def set_id(self, logid):
		""" Set the log identifier. This should be called before get_json() to
		ensure that the id is set in the returned JSON data.
		
		:param str logid: Unique identifier for the log
		"""
		
		self.meta["id"] = logid
