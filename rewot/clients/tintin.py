# -*- coding: utf-8 -*-
"""
	TinTin++ parser
	~~~~~~~~~~~~~~~
	
	TinTin++ client module to parse lines.
"""

import re

from ansi2html import Ansi2HTMLConverter


class TinTin:
	""" This TinTin class will, given a raw input line from the log, break it
	down into the necessary components and process it. The goal of processing
	these lines are to compute the delta (delay) between lines and convert any
	ANSI color sequences into the equivalent HTML tags with CSS markup.
	"""
	
	def __init__(self):
		self.ansi = Ansi2HTMLConverter()
		self.last_ts = 0
		self.client = None
	
	
	def _tintin_0_1(self, line):
		""" Parse a line from the log, format version 0.1.
		
		:param str line: Raw text of the line to parse
		:return: Parsed line
		:rtype: dict
		
		TinTin++ can (with `#format`_) create timestamps with the number of
		micro seconds since the Unix epoch. This provides an easy and precise
		measurement to use for calculating the delta for each line.
		
		.. _#format: http://tintin.sourceforge.net/manual/format.php
		
		The line begins with the timestamp, followed by a space, followed by
		the MUD text. Note that the space is required, even if there's nothing
		after it. Lines which don't match this format are presumed to have no
		timestamp and are given a delta of 0 from the last line.
		
		Example line:
		  ``1452707385328498 [ obvious exits: E ]``
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
		""" Set the specific client version to **client_string**.
		
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
		""" Entry point to parse a line based on the log format version. From
		here, the appropriate function will be called based on the version, as
		set by set_client().
		
		:param str line: Raw text of the line to parse
		:return: Parsed line
		:rtype: dict
		"""
		
		if self.client:
			return self.client(line)
		else:
			return {}
