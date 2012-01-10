#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from cssify import cssify, XpathException
import simplejson as json

class MainHandler(webapp.RequestHandler):
    def post(self):
        xpath = self.request.get('xpath')
        if xpath:
            self.response.headers['Content-Type'] = 'application/json'
            try:
                css = cssify(xpath)
            except XpathException, e:
                self.response.out.write(json.dumps({'status': 'fail', 'response': str(e)}))
            else:
                self.response.out.write(json.dumps({'status': 'pass', 'response': css}))
        else:
            self.response.out.write("Send your xpath via POST under the xpath param")

    def get(self):
        self.response.out.write("Send your xpath via POST under the xpath param")


def main():
    application = webapp.WSGIApplication([('/cssify', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
