# -*- coding: utf-8 -*-
"""
	ZMud Parser
	~~~~~~~~~~~
	
	ZMud client module to parse lines.
"""

import datetime
import re

from ansi2html import Ansi2HTMLConverter


class ZMud:
	""" This ZMud class will, given a raw input line from the log, break it
	down into the necessary components and process it. The goal of processing
	these lines are to compute the delta (delay) between lines and convert any
	ANSI color sequences into the equivalent HTML tags with CSS markup.
	"""
	
	def __init__(self):
		self.ansi = Ansi2HTMLConverter()
		self.last_dt = 0
		self.client = None
	
	
	def _zmud_0_1(self, line):
		""" Parse a line from the log, format version 0.1.
		
		:param str line: Raw text of the line to parse
		:return: Parsed line
		:rtype: dict
		
		ZMud can (with `%time`_) can create timestamps with millisecond
		precision, which will be good enough here. It doesn't appear possible
		to create `ISO 8601`_ style timestamps without multiple calls to %time
		(haven't been able to insert a 'T' between date and time), so to keep
		processing by the mud client to a minimum, a dash (-) is used instead.
		The format is then "yy-mm-dd-hh:mm:ss.z", and this is easy enough to
		parse into a datetime object to calculate deltas.
		
		.. _%time: http://www.zuggsoft.com/modules/mx_kb/kb.php?page=3&mode=doc&k=605
		.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
		
		The line begins with the timestamp, followed by a space, followed by
		the MUD text. Note that the space is required, even if there's nothing
		after it. Lines which don't match this format are presumed to have no
		timestamp and are given a delta of 0 from the last line.
		
		Example line:
		  ``16-01-13-09:25:06.438 [36mSleeping Chamber[0m``
		"""
		
		d = {"delta": 0, "show": True, "raw": line}
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
				d["delta"] = d["delta"] * 1000
			self.last_dt = dt
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
		
		if client_string == "zmud-0.1" or client_string == "zmud":
			self.client = self._zmud_0_1
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
