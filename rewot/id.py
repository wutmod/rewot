# -*- coding: utf-8 -*-
"""
	Unique ID Generator
	~~~~~~~~~~~~~~~~~~~
	
	Generate a unique identifier to reference logs.
"""

from datetime import datetime
from os.path import exists
import string


# List of numbers and letters to use in the log id
BASE_LIST = [c for c in string.digits + string.ascii_letters]
BASE_LENGTH = len(BASE_LIST)


def generate(path):
	"""	Create a base62 encoded unique identifier based on current timestamp.
	Checks **path** for an existing file with the name of the generated
	identifier to determine uniqueness.
	
	:param str path: Path to generated identifiers (files in a directory)
	:return: Unique identifier if one was able to be created
	:rtype: str or None
	
	To generate the shortest unique id possible, a datetime object is created
	based on the current timestamp. From this datetime object, starting with
	milliseconds, then appending seconds, then hours, until year, the value is
	base62 encoded and checked for an existing identifier of the same value.
	In this way can uniqueness be mostly ensured (eight requests with the same
	timestamp will result in the eighth one failing).
	"""
	
	now = datetime.utcnow()
	ts = ""
	times = (
		str(now.microsecond)[0:3],
		now.second,
		now.minute,
		now.hour,
		now.day,
		now.month,
		now.year
	)
	
	for dt in times:
		ts = int("{}{}".format(ts, dt))
		s = ""
		
		i = ts
		while i != 0:
			r = BASE_LIST[int(i % BASE_LENGTH)]
			i = int(i / BASE_LENGTH)
			s += r
		
		try:
			open("{}/{}.json".format(path, s), "x").close()
		except FileExistsError:
			pass
		else:
			return s
	
	return
