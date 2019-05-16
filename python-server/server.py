
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

import autocomplete
import autocomplete_form
import test_health
import tests


@app.route(autocomplete.methods["autocomplete_word"]["url"], methods=autocomplete.methods["autocomplete_word"]["http_methods"])
def autocomplete_word():
    request_data = dict(request.get_json())
    text = request_data["text"]

    return jsonify({"suggestions": "\n".join(autocomplete.get_suggestions_for(text))})


@app.route(autocomplete_form.methods["autocomplete_form"]["url"], methods=autocomplete_form.methods["autocomplete_form"]["http_methods"])
def autocomplete_form():
    return """
    <!DOCTYPE HTML>
    <html>
    <body style="background-color: black;">
    <div style="display: flex; flex-direction: column;">
        <input id="text" type="text" style="width: 50%; margin-top: 2em;" />
        <Input type="submit" onclick="getResponse()" style="width: 30%;margin-top: 2em;"/>
        <textarea id="result" style="width: 50%;height:30%;margin-top: 2em;" ></textarea>
    </div>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script>
    
    function getResponse() {
        $.ajax({url: '/autocomplete', data: JSON.stringify({"text": document.getElementById("text").value}), type: "POST",
            contentType: "application/json",
            success: function (data) {
                $('#result').val(data["suggestions"]);
            }
        });
    }
    </script>
    </body>
    </html>
    """


@app.route(test_health.methods["testHealth"]["url"], methods=test_health.methods["testHealth"]["http_methods"])
def testHealth():
    # request.headers.get('')
    # request.args.get('')
    # data = json.loads(list(request.form.keys())[0])
    return "Python server is up"


@app.route(tests.methods["test"]["url"], methods=tests.methods["test"]["http_methods"])
def test():
    questions = ["wh", "where is ", "where is m",
                 "numb", "number of ", "by ",
                 "ho", "how many ", "in ",
                 "against ",
                 "who is the ", "who is the ma",
                 "how much did ", "in ",
                 "Numb", "Number of ", "Number of centuries scored by ",
                 "Number of sixes by Sachin against ",
                 "Number of sixes by Dhoni against ",
                 "Number of sixes by Sachin against Pak",
                 "Who is the man of the match of Wo",
                 "How much did India score in World Cup 2011 fi"



                 ]
    output = ""
    for question in questions:
        output = output + question + "?\n"
        output = output + "\n".join(autocomplete.get_suggestions_for(question)) + "\n\n"
    return "<textarea>" + output + "</textarea>"


if __name__ == '__main__':
    app.run(host=host, port=5001, debug=show_output)

