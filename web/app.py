#!/usr/bin/env python

import sys
from flask import Flask, request, jsonify

sys.path.append('../')
from cssify.cssify import cssify, XpathException


app = Flask(__name__, static_url_path='')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route("/cssify", methods=['GET', 'POST'])
def cssify_handler():
    if request.method == 'POST':
        xpath = request.form['xpath']
        if xpath:
            try:
                css = cssify(xpath)
            except XpathException, e:
                return jsonify({'status': 'fail', 'response': str(e)})
            else:
                return jsonify({'status': 'pass', 'response': css})
        else:
            return "Send your xpath via POST under the xpath param"
    else:
        return "Send your xpath via POST under the xpath param"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
