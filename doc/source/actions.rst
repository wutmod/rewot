Actions
=======

.. contents::
	:depth: 3


Actions
-------

Actions are special lines inserted into the log for the parser to handle.
Action lines begin with ``#!``.


``#!client``
^^^^^^^^^^^^

Specify the client parser and version to use::

	#!client tintin-0.1


``#!delay``
^^^^^^^^^^^

Insert a delay in the replay::

	#!delay 2.4


``#!mark``
^^^^^^^^^^

Insert an HTML horizontal rule (``<hr>``)::

	#!mark


``#!say``
^^^^^^^^^

Print a line of text in the replay::

	#!say hello there


Comments
--------

Comment lines start with ``##`` and are ignored by the parser and can be used to
provide commentary of the log, but they are not rendered for the replay like the
``#!say`` action is. Example::

	## this is a comment
