#!/usr/bin/env python

import os
import time
import subprocess
import tempfile
import zipfile
import urllib
import logging

logging.basicConfig(level=logging.DEBUG)


class AppEngineSetup(object):
    """ Download and run your app using Google App Engine """

    def __init__(self):
        self.appengine_url = "http://googleappengine.googlecode.com/files/google_appengine_1.7.5.zip"
        self.startup_timeout = 90

    def download(self):
        logging.info("Downloading App Engine")
        tmpdir = tempfile.mkdtemp(prefix="app_engine.")
        filename = urllib.urlretrieve(self.appengine_url)[0]
        logging.info("Extracting App Engine")
        appengine_zip = zipfile.ZipFile(filename)
        for zipped_filename in appengine_zip.namelist():
            if zipped_filename.endswith('/'):
                os.makedirs(os.path.join(tmpdir, zipped_filename))
                continue
            destination = open(os.path.join(tmpdir, zipped_filename), 'wb')
            try:
                zipped_file = appengine_zip.open(zipped_filename)
                while True:
                    buff = zipped_file.read(1024 * 1024)
                    if not buff:
                        break
                    destination.write(buff)
            finally:
                destination.close()
        logging.info("App Engine is ready to use in path %s", tmpdir)
        return tmpdir

    def run(self, appengine_location, appengine_app_path, extra_args=[]):
        cmd = ["python",
               os.path.join(appengine_location,
                            "google_appengine",
                            "dev_appserver.py"),
               appengine_app_path] + extra_args

        logging.info("Running App Engine with cmd: %s", " ".join(cmd))
        proc = subprocess.Popen(cmd)
        logging.info("App Engine is starting; PID is %d", proc.pid)

        poll_wait = 0.5
        for x in xrange(int(self.startup_timeout // poll_wait)):
            if proc.poll() is not None:
                raise Exception("App Engine exited with code %d."
                                % proc.returncode)
            try:
                urllib.urlopen("http://localhost:8080")
            except IOError:
                logging.info("App Engine is not ready yet. Waiting...")
                time.sleep(poll_wait)
                continue
            logging.info("App Engine is ready for testing!")
            return proc
        raise Exception("Done waiting for AppEngine to run; "
                        "waited ~%ds." % self.startup_timeout)

if __name__ == "__main__":
    admin = AppEngineSetup()
    downloaded = admin.download()
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    aeapp_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    process = admin.run(downloaded, aeapp_path)
