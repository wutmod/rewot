Client Specific Parsers
~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
	:maxdepth: 3
	
	TinTin++ <clients.tintin>
	ZMud <clients.zmud>


Each MUD client has a different set of capabilities. Because of this, it's
impossible to expect the same log format from each client. Therefore, there
should be a relatively easy way to add support for more clients, or to further
extend the existing ones.

This is accomplished with client modules. Each client module may have multiple
versions of the log format, specified with **client_string**, in order to
maintain compatability as log formats change.

The client modules are responsible for taking the raw text from the log and
generating a dict with the following structure::

	{
	    "show": True,
	    "delta": 1.832,
	    "line": "<span class=\"ansi36\">Aringill Bakery</span>"
	}

ANSI color sequences should be converted using `ansi2html`_. In some clients
this may close off the color sequences at the end of the line instead of at the
end of the block, this is due to the nature of the parser being line based.
While this could probably be overcome, it's not a priority at this time.

Client modules must have two public interfaces:

* ``set_client(client_string)``
	**client_string** describes the version of the log format, in the style of
	*client-version*, for example::
	
		tintin-0.1
	
	Either *True* or *False* must be returned to denote successful or unsuccessful
	setting of the client version.

* ``parse(line)``
	This shall be the main entry point for the parser, using **line** as the
	text to parse. From here, all the necessary actions in parsing the line
	should be performed, and a dict in the format described above shall be
	returned.

.. _ansi2html: https://pypi.python.org/pypi/ansi2html
