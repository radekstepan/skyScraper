#!/usr/bin/python
# -*- coding: utf -*-

# framework
import os
from flask import Flask, request

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)

from webkit import Webkit
w = Webkit()

@app.route('/get', methods=["POST"])
def get():
    '''curl -s --data "url=http://localhost:5001/system/test" http://localhost:5003/get'''
    url = request.form['url']
    return os.popen('python webkit.py method=GET url=%s' % url).read()

@app.route('/post', methods=["POST"])
def post():
    '''curl -s --data "url=http://localhost/test/welcome.php&name=Radek&age=26" http://localhost:5003/post'''
    url = request.form['url']

    # paramize form params from dict
    params = dict(request.form)
    form = ''
    for key, value in params.items():
        if key != 'url':
            form += "'%s':'%s'," % (key, value[0])

    if form:
        form = "form={" + form[:-1] + "}"
    
    return os.popen('python webkit.py method=POST url=%s %s' % (url, form)).read()

if __name__ == '__main__':
    app.run(port=5003)