#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
from flask import Flask
try:
    from App import launchWindow
except ImportError:
    from .App import launchWindow

# create the flask server to serve the bossweb Application. 
server = Flask(__name__)
app_thread = threading.Thread(target=launchWindow, kwargs={'url':"http://127.0.0.1:5000/"})
app_thread.start()

@server.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World"


if __name__ == '__main__': 
    server.run(debug=True, use_reloader=True)