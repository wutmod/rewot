JSON Data
=========

.. contents::
	:depth: 2


Introduction
------------

`JSON`_ is used as the data format for the parsed logs. Using JSON, it's easy to
describe the data as needed without requiring a parser to be implemented in
the browser, or any other replay viewer that might be created.

.. _JSON: http://www.json.org

Sample
------

::

	{
		"log": [
			{
				"lineno": 59,
				"delta": 0.0,
				"show": true,
				"line": "<span class=\"ansi33\">A silent, black-robed figure watches you from afar.</span>"
			},
			{
				"lineno": 60,
				"delta": 0,
				"show": true,
				"line": "16-01-13-08:00:46.760"
			},
			{
				"lineno": 64,
				"delta": 0.0,
				"show": true,
				"line": "o HP:Healthy DP:Bursting MV:Full &gt;"
			}
		],
		"meta": {
			"title": "zmud demo",
			"id": "5e",
			"player": "Anonymous"
		}
	}
