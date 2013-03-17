cssify
======

Get your XPATHs translated to css automatically! (don't go to crazy on what you
want to translate, this script is smart but won't do your breakfast).

.. image:: https://travis-ci.org/santiycr/cssify.png?branch=master
   :alt: [Build Status]
   :target: https://travis-ci.org/santiycr/cssify

.. image:: https://saucelabs.com/buildstatus/cssify
   :alt: [Sauce Status]
   :target: https://saucelabs.com/u/cssify

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

  
Testing and contributing
------------------------

Supported and unsupported cases are documented by tests. If you have a request
or a contribution for new conversions, include a test that proves the issue and
solution and send a pull request.

To run all unit tests locally::

  $ nosetests tests/test_cssify.py

To run all Selenium tests locally (some env variables are necessary)::

  $ nosetests tests/test_cssify_web.py
