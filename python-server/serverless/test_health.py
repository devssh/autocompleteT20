methods = {"testHealth": {
    "url": "/testHealth",
    "http_methods": ["GET", "POST"]
    }
}


def testHealth():
    # request.headers.get('')
    # request.args.get('')
    # data = json.loads(list(request.form.keys())[0])
    return "Python server is up"
