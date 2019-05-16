methods = {"autocomplete_form": {
    "url": "/",
    "http_methods": ["GET"]
    }
}


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
