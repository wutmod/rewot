ZMud
====

.. contents::
	:depth: 2


Introduction
------------

`ZMud`_ is the Windows Mud client by `Zugg Software`_. It has since been
deprecated in favor of `CMud`_, yet it still has a sizable user base. The ZMud
script used for ReWoT should also work for CMud.


.. _ZMud: http://www.zuggsoft.com/page.php?file=zmud/zmudinfo.htm
.. _Zugg Software: http://www.zuggsoft.com
.. _CMud: http://forums.zuggsoft.com/index.php?p=cmud


Script
------

The script consists of a class, **rewot**, and a subclass **triggers**. The
**rewot** class contains the necessary aliases:

* ``reek``: Stop the logging. This will disable the triggers and close the file.

* ``reline``: This alias isn't one that the user needs to worry about. It's used
  internally by the triggers to write lines to the log.

* ``relog <fileno> <logfile>``: Start the logging. Both **fileno** and
  **logfile** are required. This alias opens the file, writes the ``#!client``
  action and enables the triggers.
  
  * **fileno** : This is the require file handle number, passed to `#file`_.
    The script has no way of knowing what, if any, file handles might be used
    by other scripts, so it is left to the user to determine the number to use.
    The number must be between 1 and 5 and not already be used.
  
  * **logfile** : The filename to log to. This will be saved in the ZMud
    directory and has some constraints as listed by `#file`_.

.. _#file: http://www.zuggsoft.com/modules/mx_kb/kb.php?page=3&mode=doc&k=292

:download:`rewot.zmud.txt <rewot.zmud.txt>`::

	#CLASS {rewot}
	#ALIAS reline {#var rewot/ts %time( "yy-mm-dd-hh:mm:ss.z");#write @rewot/fileno {@ts" %0"}}
	#ALIAS relog {#var rewot/fileno %1;#var rewot/logfile %2;#file @rewot/fileno @rewot/logfile;#write @rewot/fileno {};#write @rewot/fileno {"#!client zmud-0.1"};#t+ rewot/triggers}
	#ALIAS reek {#t- rewot/triggers;#close @rewot/fileno}
	#CLASS 0
	
	#CLASS {rewot|triggers}
	#TRIGGER {*} {reline "%0"} "" {prompt|notrig|color}
	#TRIGGER {$} {reline "%0"} "" {notrig|color}
	#CLASS 0

