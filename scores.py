import requests

api_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"


def get_scores(date):
    scoreboard = requests.get(api_url, params={'dates': date}).json()

    if not scoreboard["events"]:
        return None, None

    competitors = scoreboard["events"][0]["competitions"][0]["competitors"]

    if competitors[0]["homeAway"] == "home":
        competitors.reverse()

    teams = [competitor["team"]["name"] for competitor in competitors]
    scores = [[sum(line_score["value"] for line_score in competitor["linescores"][:i + 1]) for i in
               range(len(competitor["linescores"]))] for competitor in competitors]

    return teams, scores
