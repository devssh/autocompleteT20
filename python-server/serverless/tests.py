methods = {"test": {
    "url": "/test",
    "http_methods": ["GET"]
}
}


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
