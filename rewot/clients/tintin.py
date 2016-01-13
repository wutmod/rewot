# -*- coding: utf-8 -*-
"""
	rewot.clients.tintin
	~~~~~~~~~~~~~~~~~~~~
	
	TinTin++ line parser.
"""

import re

from ansi2html import Ansi2HTMLConverter


class TinTin:
	def __init__(self):
		""" Create the TinTin object. """
		
		self.ansi = Ansi2HTMLConverter()
		self.last_ts = 0
		self.client = None
	
	
	def _tintin_0_1(self, line):
		""" Parse a line from the log.
		
		:param str line: Raw text of the line to parse
		:return: Parsed line
		:rtype: dict
		"""
		
		d = {"delta": 0, "show": True}
		
		m = re.match(r"^(?P<ts>\d+) (?P<line>.*)$", line)
		if m:
			ts = float(m.groupdict().get("ts")) / 1000000
			d["line"] = m.groupdict().get("line")
			
			if self.last_ts:
				d["delta"] = ts - self.last_ts
				if d["delta"] < 0:
					d["delta"] = 0
				elif d["delta"] > 4:
					d["delta"] = 4
			self.last_ts = ts
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
		
		if client_string == "tintin-0.1" or client_string == "tintin":
			self.client = self._tintin_0_1
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
