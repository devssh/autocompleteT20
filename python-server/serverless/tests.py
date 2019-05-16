methods = {"test": {
    "url": "/test",
    "http_methods": ["GET"]
}
}


def test():
    questions = ["wh", "where is"]
    output = ""
    for question in questions:
        output = output + question + "?\n" + "\n".join(autocomplete.get_suggestions_for(question)) + "\n\n"
    return "<textarea>" + output + "</textarea>"
