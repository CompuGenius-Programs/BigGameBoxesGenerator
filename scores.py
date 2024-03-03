import espn_scoreboard


def get_scores(date):
    scoreboard = espn_scoreboard.ESPNScoreboard("football", "nfl").get_scoreboard(date)
    competitors = scoreboard["events"][0].competitions[0].competitors

    if competitors[0].home_away == "home":
        competitors.reverse()

    teams = [competitor.team.name for competitor in competitors]
    scores = [competitor.line_scores for competitor in competitors]

    return teams, scores
