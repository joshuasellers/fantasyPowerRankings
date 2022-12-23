import json
import requests
import consts
import os
from fpdf import FPDF, HTMLMixin


class MyFPDF(FPDF, HTMLMixin):
    pass


def user_name(userid):
    response = requests.get("https://api.sleeper.app/v1/user/" + userid)
    json_response = json.loads(response.text)
    return consts.OWNER_NAMES()[json_response['username']]


def league_owners():
    response = requests.get("https://api.sleeper.app/v1/league/" + consts.LEAGUE_ID() + "/rosters")
    json_response = json.loads(response.text)
    owners = []
    for team in json_response:
        owners.append(user_name(team['owner_id']))
    return ', '.join(owners)


def league_name():
    response = requests.get("https://api.sleeper.app/v1/league/" + consts.LEAGUE_ID())
    json_response = json.loads(response.text)
    return json_response['name']


def roster_id_to_owner(id):
    response = requests.get("https://api.sleeper.app/v1/league/" + consts.LEAGUE_ID() + "/rosters")
    json_response = json.loads(response.text)
    for team in json_response:
        if team['roster_id'] == id:
            return user_name(team['owner_id'])


def matchups():
    response = requests.get("https://api.sleeper.app/v1/league/" + consts.LEAGUE_ID() + "/matchups/" + consts.WEEK())
    json_response = json.loads(response.text)
    matchups = []
    for matchup in json_response:
        for opponent in json_response:
            if matchup['matchup_id'] == opponent['matchup_id'] and matchup['roster_id'] != opponent['roster_id']:
                matchups.append([matchup, opponent])
                json_response.remove(opponent)
    return matchups


def matchup_results(matchups):
    mr = []
    for i in range(0, len(matchups)):
        mr.append("Matchup " + str(i+1))
        mr.append(roster_id_to_owner(matchups[i][0]['roster_id']) +
              " scored " + str("%.2f" % sum(matchups[i][0]['starters_points'])) + " points")
        mr.append(roster_id_to_owner(matchups[i][1]['roster_id']) +
              " scored " + str("%.2f" % sum(matchups[i][1]['starters_points'])) + " points")
    return mr


if __name__ == '__main__':
    filename = 'week' + str(consts.WEEK()) + 'results.pdf'
    if os.path.exists(filename):
        os.remove(filename)
    pdf = MyFPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    html = """
            <h1><span><strong>""" + league_name() + """</strong></span></h1>
            <hr/>
            <p><em><span>""" + league_owners() + """</span></em></p>
            <hr/>
            <h2>Week """ + str(consts.WEEK()) + """ Results</h2>
    """
    results = matchup_results(matchups())
    for i in range(0, len(results)):
        if i % 3 == 0:
            html += """<h3>""" + results[i] + """ </h3>"""
        else:
            html += """<p>""" + results[i] + """ </p>"""
    pdf.write_html(html)
    pdf.output(filename)
