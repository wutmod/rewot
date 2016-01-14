TinTin++
========

.. contents::
	:depth: 2


Introduction
------------

`TinTin++`_ is the prominent Mud client for Linux. There is also a WinTin++
available from the same developers, however it is currently unknown if this
script functions properly with WinTin++.

.. _TinTin++: http://tintin.sourceforge.net


Script
------

This version of the script is very simple, and doesn't yet offer control to turn
it on or off, nor to choose the filename. It uses `#event`_ to log everything to
*rewot.log*. Note that this script does not include the ``#!client`` action, so
that will have to be included manually::

	#!client tintin-0.1

.. _#event: http://tintin.sourceforge.net/manual/event.php

:download:`rewot.tintin.txt <rewot.tintin.txt>`::

	#event {RECEIVED LINE} {#format line {%U %0} {%0};#line log rewot.log {$line}}
	#event {SEND OUTPUT} {#format line {%U %0} {%0};#line log rewot.log {$line}}

