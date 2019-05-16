
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

import json
import sys
import logging

host = "0." + "0.0.0"
show_output = True

app = Flask(__name__)
# CORS(app, resources={r"*": {"origins": "*"}})
app.logger.setLevel(logging.DEBUG)
app.logger.debug('Server started successfully')

sys.path.insert(0, 'serverless')

