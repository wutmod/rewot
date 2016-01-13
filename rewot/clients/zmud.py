# -*- coding: utf-8 -*-
"""
	rewot.clients.zmud
	~~~~~~~~~~~
	
	ZMud++ line parser.
	
	:copyright: Copyright 2016 by the ReWoT team, see AUTHORS.rst.
	:license: MIT, see LICENSE for details.
"""

import datetime
import re

from ansi2html import Ansi2HTMLConverter


class ZMud:
	def __init__(self):
		""" Create the ZMud object. """
		
		self.ansi = Ansi2HTMLConverter()
		self.last_dt = 0
		self.client = None
	
	
	def _zmud_0_1(self, line):
		""" Parse a line from the log.
		
		:param str line: Raw text of the line to parse
		:return: Parsed line
		:rtype: dict
		"""
		
		d = {"delta": 0, "show": True}
		m = re.match(r"^(?P<ts>(?:\d+-){3}\d+:\d+:\d+\.\d+) (?P<line>.*)$", line)
		if m:
			dt = datetime.datetime.strptime(
				m.groupdict().get("ts"),
				"%y-%m-%d-%H:%M:%S.%f"
			)
			d["line"] = m.groupdict().get("line")
			
			if self.last_dt:
				d["delta"] = dt - self.last_dt
				if d["delta"].total_seconds() < 0:
					d["delta"] = 0
				elif d["delta"].total_seconds() > 4:
					d["delta"] = 4
				else:
					d["delta"] = d["delta"].total_seconds()
			self.last_dt = dt
		else:
			d["line"] = line
		
		d["line"] = self.ansi.convert(d["line"], full=False)
		
		return d
	
		
	def set_client(self, client_string):
		""" Set the specific client version.
		
		:param str client_string: Client version string
		:return: Success
		:rtype: True or False
		"""
		
		if client_string == "zmud-0.1" or client_string == "zmud":
			self.client = self._zmud_0_1
			return True
		else:
			return False
	
	
	def parse(self, line):
		""" Parse a line from the log with the appropriate client format.
		
		:param str line: Raw text of the line to parse
		:return: Parsed line
		:rtype: dict
		"""
		
		if self.client:
			return self.client(line)
		else:
			return {}
