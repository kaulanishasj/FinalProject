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
import webapp2
import os
import jinja2
import logging
import json
import urllib
import csv
import httplib2
from apiclient.discovery import build

# this is used for constructing URLs to google's APIS
from googleapiclient.discovery import build

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# Import the Flask Framework
from flask import Flask, request
app = Flask(__name__)

def get_all_data():    
    # open the data stored in a file called "death.csv"
    try:
        with open("data/death.csv", 'rb') as f:
            read = csv.reader(f)
            response = []
            for row in read:
                #logging.info(row)
                response.append(row)
        #first 4 rows are meta-data
        return dataDict(response[4:])

    except IOError:
        logging.info("failed to load file")        

def dataDict(d):
    data = {}
    for row in d:
        state = row[0]
        count = float(row[1])
        data[state] = count
    return data

    
@app.route('/')
def index():
    data = get_all_data()
    logging.info(data)
    variables = {'data':data}
    template = JINJA_ENVIRONMENT.get_template('templates/index.html')
    return template.render(variables)

@app.route('/about')
def about():
    template = JINJA_ENVIRONMENT.get_template('templates/about.html')
    return template.render()


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500