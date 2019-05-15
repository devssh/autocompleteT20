server = open("server.py", 'w')

initial_setup = """
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

"""

import sys
sys.path.insert(0, 'serverless')

server.write(initial_setup)
server.close()

server1 = open("server.py", 'a')

import subprocess

proc = subprocess.Popen(["ls serverless"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
services = out.decode("utf-8").split("\n")
services = list(filter(len, services))
services = [service.split(".py")[0] for service in services if not service.startswith("__")]
imports = ["import " + service + "\n" for service in services]
exec("".join(imports))

from dill.source import getsource

controller_methods = []
for service in services:
    controller_method_names = list(eval(service+".methods").keys())
    for controller_method_name in controller_method_names:
        controller_method = getsource(eval(service + "." + controller_method_name))
        controller_methods = [*controller_methods,
                              "\n\n@app.route(" + service + ".methods[\"" + controller_method_name + "\"][\"url\"]," +
                              " methods=" + service + ".methods[\"" + controller_method_name +"\"][\"http_methods\"])\n" +
                              controller_method
                              ]

footer = """

if __name__ == '__main__':
    app.run(host=host, port=5001, debug=show_output)

"""

server1.writelines([*imports, *controller_methods, footer])
server1.close()
