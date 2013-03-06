cssify
======

Get your XPATHs translated to css automatically! (don't go to crazy on what you
want to translate, this script is smart but won't do your breakfast).

.. image:: https://travis-ci.org/santiycr/cssify.png?branch=master
   :alt: [Build Status]
   :target: https://travis-ci.org/santiycr/cssify

Usage
-----

**New!** Use cssify from a browser::

http://cssify.appspot.com

From the console::

  $ ./cssify.py '//a'
  a
  $ ./cssify.py '//a[@id="bleh"]'
  a#bleh

From python::

  >>> from cssify import cssify
  >>> cssify('//a')
  'a'
  >>> cssify('//a[@id="bleh"]')
  'a#bleh'

  
Known Issues and unsupported XPATHs
-----------------------------------

Known issues should have failing tests. Tests are part of the script itself.
They use the `doctest <http://docs.python.org/library/doctest.html>`_ format.
To run tests and see any known issue (failing test), just run cssify with the
-t flag::

  $ ./cssify.py -t
