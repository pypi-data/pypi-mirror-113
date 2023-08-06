Pygments__ syntax highlighting styles for dark and light backgrounds

__ https://pygments.org/

.. image:: https://raw.githubusercontent.com/LivingLogic/LivingLogic.Python.PygLL/master/PygLL.png


Installation
============

Install with::

	$ pip install pygll


After installation, two new Pygments styles are available:

=============================== =====================
Python class                    Plugin name
=============================== =====================
``pygll.LivingLogicLightStyle`` ``livinglogic-light``
``pygll.LivingLogicDarkStyle``  ``livinglogic-dark``
=============================== =====================


Usage with Sphinx
=================

If you want to use this Pygments style with Sphinx put the following in your
``conf.py``::

	pygments_style = 'livinglogic-light'

Whether and how you can specify both styles to let the browser automatically
switch them depending on the current OS color scheme depends on the HTML theme
you're using.


History
=======

0.1 (2021-07-23)
----------------

Initial release.