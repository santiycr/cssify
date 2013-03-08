#!/usr/bin/env python

import os
import time
import subprocess
import tempfile
import zipfile
import urllib
from random import randint
import logging

logging.basicConfig(level=logging.DEBUG)


class SauceConnectSetup(object):
    """ Download and run Sauce Connect """

    def __init__(self):
        self.connect_url = "http://saucelabs.com/downloads/Sauce-Connect-latest.zip"
        self.startup_timeout = 90

    def download(self):
        logging.info("Downloading Sauce Connect")
        tmpdir = tempfile.mkdtemp(prefix="sauce_connect.")
        filename = urllib.urlretrieve(self.connect_url)[0]
        logging.info("Extracting Sauce Connect")
        connect_zip = zipfile.ZipFile(filename)
        for zipped_filename in connect_zip.namelist():
            destination = open(os.path.join(tmpdir, zipped_filename), 'wb')
            try:
                destination.write(connect_zip.read(zipped_filename))
            finally:
                destination.close()
        logging.info("Sauce Connect is ready to use in path %s", tmpdir)
        return tmpdir

    def run(self, connect_location, extra_args=[]):
        readyfile = os.path.join(connect_location,
                                 "ready_%s" % randint(0, 10000))
        cmd = ["java", "-jar",
               os.path.join(connect_location, "Sauce-Connect.jar"),
               "--readyfile", readyfile
               ] + extra_args
        if (os.environ.get('TRAVIS') and
            os.environ.get('HAS_JOSH_K_SEAL_OF_APPROVAL')):
            cmd.append("--tunnel-identifier")
            cmd.append(os.environ['TRAVIS_BUILD_ID'])

        logging.info("Running Sauce Connect with cmd: %s", " ".join(cmd))
        cmd.append(os.environ['SAUCE_USERNAME'])
        cmd.append(os.environ['SAUCE_ACCESS_KEY'])
        proc = subprocess.Popen(cmd)
        logging.info("Sauce Connect is starting; PID is %d", proc.pid)

        poll_wait = 0.5
        for x in xrange(int(self.startup_timeout // poll_wait)):
            if proc.poll() is not None:
                raise Exception("Sauce Connect script exited with code %d."
                                % proc.returncode)
            if os.path.exists(readyfile):
                logging.info("Sauce Connect is ready for testing!")
                return proc
            if x % 5:
                logging.info("Sauce Connect is not ready yet. Waiting...")
            time.sleep(poll_wait)
        raise Exception("Done waiting for tunnel to become ready; "
                        "waited ~%ds." % self.startup_timeout)

if __name__ == "__main__":
    admin = SauceConnectSetup()
    downloaded = admin.download()
    process = admin.run(downloaded)
