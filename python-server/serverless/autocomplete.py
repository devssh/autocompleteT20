methods = {"autocomplete_word": {
    "url": "/autocomplete",
    "http_methods": ["POST"]
}
}

data_dir = "data/"
import pandas as pd

players_df = pd.read_csv(data_dir + 'players.txt', delimiter="\t")
players_df["Country"] = "Other"
players_df.loc[players_df["Commonly Called as"].str.startswith("Sachin"), "Country"] = "India"
stadiums_df = pd.read_csv(data_dir + 'stadiums.txt', delimiter="\t")
teams = pd.read_csv(data_dir + 'teams.txt', delimiter="\t")["Names"].tolist()
keywords = pd.read_csv(data_dir + 'keywords.txt', delimiter="\t")["Keywords"].tolist()
stadiums = stadiums_df["Names"].tolist()
cities = stadiums_df["City"].tolist()
players = list({*players_df["Formal Name"].tolist(), *players_df["Commonly Called as"].tolist()})

import inflect

# or alternatively use NNS for plural detection in NLTK Part of Speech Tagging below
inflect = inflect.engine()
plural_keywords = list(
    reversed([word for word in keywords if len(word.split(" ")) < 2 and not inflect.singular_noun(word) is False]))

import nltk

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
superlative_keywords = []
for word in keywords:
    tagged_sent = nltk.pos_tag(nltk.word_tokenize("who is the " + word))
    superlative = False
    if tagged_sent[3][1] in ["JJS", "JJ"] or len(word.split(" ")) > 2:
        superlative = True
    if superlative:
        superlative_keywords = [*superlative_keywords, word]

import language_check

tool = language_check.LanguageTool('en-US')
superlative_keywords = [keyword for keyword in superlative_keywords if
                        len(tool.check("Who is the " + keyword + "?")) == 0]


def filter_with(keyword, some_list):
    if len(keyword.strip()) == 0:
        return some_list
    return [elem for elem in some_list if elem.lower().startswith(keyword)]


def get_suggestions_for(text):
    current_word = text.split(" ")[-1].lower()
    context = " ".join(text.split(" ")[:-1]).lower().strip()
    applicable_keywords = filter_with(current_word, keywords)
    applicable_stadiums = filter_with(current_word, stadiums)
    applicable_city = filter_with(current_word, cities)
    applicable_players = filter_with(current_word, players)
    applicable_teams = filter_with(current_word, teams)
    applicable_countable_keywords = filter_with(current_word, plural_keywords)
    applicable_superlative_keywords = filter_with(current_word, superlative_keywords)

    suggestions = [*applicable_keywords, *applicable_stadiums]
    if context.endswith("where is"):
        suggestions = [*applicable_stadiums]

    if context.endswith("number of"):
        suggestions = [*applicable_countable_keywords]

    if context.endswith("by"):
        suggestions = [*applicable_players]

    if context.endswith("how many"):
        suggestions = [*applicable_countable_keywords]

    if context.endswith("in"):
        suggestions = [*applicable_stadiums, *applicable_city]

    if context.endswith("who is the"):
        suggestions = [*applicable_superlative_keywords]

    if context.endswith("how much did"):
        suggestions = [*applicable_players, *applicable_teams]

    if context.endswith("against"):
        batsman = [player for player in players if player.lower() in context]
        if len(batsman) > 0:
            batsman_in_context = batsman[-1]
            from_country = players_df.loc[
                players_df["Formal Name"].str.lower().str.startswith(batsman_in_context), "Country"].tolist()
            if len(from_country) == 0:
                from_country = players_df.loc[
                    players_df["Commonly Called as"].str.lower().str.startswith(batsman_in_context.lower()), "Country"].tolist()
            from_country = from_country[0].lower()

            applicable_teams = [team for team in applicable_teams if not team.lower() in [from_country]]
        suggestions = [*applicable_teams]

    return suggestions[0:6]


def autocomplete_word():
    request_data = dict(request.get_json())
    text = request_data["text"]

    return jsonify({"suggestions": "\n".join(autocomplete.get_suggestions_for(text))})
