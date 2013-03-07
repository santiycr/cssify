#!/usr/bin/env python

import os
import time
import subprocess
import tempfile
import zipfile
import urllib
from random import randint


class SauceConnectSetup(object):
    """ Takes care of downloading and running Connect """
    def __init__(self):
        self.connect_url = "http://saucelabs.com/downloads/Sauce-Connect-latest.zip"
        self.startup_timeout = 90

    def download(self):
        tmpdir = tempfile.mkdtemp(prefix="sauce_connect.")
        filename = urllib.urlretrieve(self.connect_url)[0]
        zipfile.ZipFile(filename).extractall(tmpdir)
        return tmpdir

    def run(self, connect_location, extra_args=[]):
        readyfile = "ready_%s" % randint(0, 10000)
        cmd = ["java", "-jar", "%s/Sauce-Connect.jar" % connect_location,
               "--readyfile", readyfile
               ] + extra_args
        if os.environ['TRAVIS_BUILD_ID']:
            cmd.append("--tunnel-id")
            cmd.append(os.environ['TRAVIS_BUILD_ID'])

        print("Sauce Connect cmd: %s" % " ".join(cmd))
        cmd.append(os.environ['SAUCE_USERNAME'])
        cmd.append(os.environ['SAUCE_ACCESS_KEY'])
        proc = subprocess.Popen(cmd)
        print("Sauce Connect is starting; PID is %d" % proc.pid)

        poll_wait = 0.5
        for x in xrange(int(self.startup_timeout // poll_wait)):
            if proc.poll() is not None:
                raise Exception("Sauce Connect script exited with code %d."
                                % proc.returncode)
            if os.path.exists(readyfile):
                print("Sauce Connect is ready for testing!")
                return proc
            time.sleep(poll_wait)
        raise Exception("Done waiting for tunnel to become ready; "
                        "waited ~%ds." % self.startup_timeout)

if __name__ == "__main__":
    admin = SauceConnectSetup()
    downloaded = admin.download()
    process = admin.run(downloaded)
