methods = {"autocomplete_word": {
    "url": "/autocomplete",
    "http_methods": ["POST"]
}
}

data_dir = "data/"
import pandas as pd

players_df = pd.read_csv(data_dir + 'players.txt', delimiter="\t")
stadiums_df = pd.read_csv(data_dir + 'stadiums.txt', delimiter="\t")
teams = pd.read_csv(data_dir + 'teams.txt', delimiter="\t")["Names"].tolist()
keywords = pd.read_csv(data_dir + 'keywords.txt', delimiter="\t")["Keywords"].tolist()
stadiums = stadiums_df["Names"].tolist()
city = stadiums_df["City"].tolist()
players = [*players_df["Formal Name"].tolist(), *players_df["Commonly Called as"].tolist()]


def get_suggestions_for(text):
    current_word = list(filter(len, text.split(" ")))[-1].lower()
    context = " ".join(text.split(" ")[:-1]).lower().strip()
    applicable_keywords = [keyword for keyword in keywords if keyword.lower().startswith(current_word)]
    applicable_stadiums = [stadium for stadium in stadiums if stadium.lower().startswith(current_word)]
    applicable_players = [player for player in players if player.lower().startswith(current_word)]
    applicable_teams = [team for team in teams if team.lower().startswith(current_word)]

    suggestions = [*applicable_keywords, *applicable_stadiums]
    if context.endswith("where is"):
        suggestions = [*applicable_stadiums]

    if context.endswith("number of"):
        suggestions = ["players", "centuries", "matches", "sixes", "boundaries"]
    if context.endswith("by"):
        suggestions = [*players]

    if context.endswith("how many"):
        suggestions = ["players", "centuries", "matches"]
    if context.endswith("in"):
        suggestions = [*stadiums, *city]

    if context.endswith("against"):
        suggestions = [*teams]

    if context.endswith("who is the"):
        suggestions = ["man of the match", "best", "top"]
    if context.endswith("ma"):
        suggestions = ["man of the match"]

    if context.endswith("how much did"):
        suggestions = [*players, teams]

    return suggestions


def autocomplete_word():
    request_data = dict(request.get_json())
    text = request_data["text"]

    return jsonify({"suggestions": "\n".join(autocomplete.get_suggestions_for(text))})
