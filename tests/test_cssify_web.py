#!/usr/bin/python

import os
import sys
import new
from random import randint
import base64
import json
import httplib
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from data import SUPPORTED, UNSUPPORTED


class CssifyTest(unittest.TestCase):
    __test__ = False

    def setUp(self):
        self.caps['name'] = 'Testing cssify'
        self.username = os.environ['SAUCE_USERNAME']
        self.key = os.environ['SAUCE_ACCESS_KEY']
        if (os.environ.get('TRAVIS') and
            os.environ.get('HAS_JOSH_K_SEAL_OF_APPROVAL')):
            self.caps['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
            self.caps['build'] = os.environ['TRAVIS_BUILD_NUMBER']
            self.caps['tags'] = [os.environ['TRAVIS_PYTHON_VERSION'], 'CI']
        hub_url = "%s:%s@ondemand.saucelabs.com:80" % (self.username, self.key)
        self.url = 'http://localhost:8080/'

        self.driver = webdriver.Remote(desired_capabilities=self.caps,
                                       command_executor="http://%s/wd/hub" % hub_url)
        self.jobid = self.driver.session_id
        print "Sauce Labs job: https://saucelabs.com/jobs/%s" % self.jobid
        self.driver.implicitly_wait(30)

    def report_test_result(self):
        base64string = base64.encodestring('%s:%s'
                                           % (self.username, self.key))[:-1]
        result = json.dumps({'passed': sys.exc_info() == (None, None, None)})
        connection = httplib.HTTPConnection("saucelabs.com")
        connection.request('PUT',
                           '/rest/v1/%s/jobs/%s' % (self.username, self.jobid),
                           result,
                           headers={"Authorization": "Basic %s" % base64string})
        result = connection.getresponse()
        return result.status == 200

    def test_supported_cssify(self):
        for path, cssified in SUPPORTED:
            self.driver.get(self.url)
            xpath = self.driver.find_element_by_id('xpath')
            xpath.send_keys(path)
            xpath.submit()
            css = WebDriverWait(self.driver, 30).until(
                lambda driver: driver.find_element_by_id("css"))
            self.assertEqual(css.get_attribute("value"), cssified)

    def test_unsupported_cssify(self):
        for path in UNSUPPORTED:
            self.driver.get(self.url)
            self.assertTrue("cssify" in self.driver.title)
            xpath = self.driver.find_element_by_id('xpath')
            xpath.send_keys(path)
            xpath.submit()
            fail = WebDriverWait(self.driver, 30).until(
                lambda driver: driver.find_element_by_class_name("fail"))
            self.assertEqual("Invalid or unsupported Xpath: %s" % path,
                             fail.text)

    def tearDown(self):
        self.driver.quit()
        self.report_test_result()


PLATFORMS = [
    {'browserName': 'firefox',
     'version': '19',
     'platform': 'LINUX',
     },
    {'browserName': 'firefox',
     'version': '19',
     'platform': 'XP',
     },
    {'browserName': 'firefox',
     'version': '19',
     'platform': 'VISTA',
     },
    {'browserName': 'chrome',
     'platform': 'LINUX',
     },
    {'browserName': 'chrome',
     'platform': 'XP',
     },
    {'browserName': 'chrome',
     'platform': 'VISTA',
     },
    {'browserName': 'internet explorer',
     'version': '10',
     'platform': 'WIN8',
     },
    {'browserName': 'internet explorer',
     'version': '9',
     'platform': 'VISTA',
     },
    {'browserName': 'internet explorer',
     'version': '8',
     'platform': 'XP',
     },
    {'browserName': 'safari',
     'version': '6',
     'platform': 'Mac 10.8',
     },
]

classes = {}
for platform in PLATFORMS:
    d = dict(CssifyTest.__dict__)
    name = "%s_%s_%s_%s" % (CssifyTest.__name__,
                            platform['browserName'],
                            platform.get('platform', 'ANY'),
                            randint(0, 999))
    d.update({'__test__': True,
              'caps': platform,
              })
    classes[name] = new.classobj(name, (CssifyTest,), d)

globals().update(classes)
