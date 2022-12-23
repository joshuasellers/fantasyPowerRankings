import json
import requests
import consts
from fpdf import FPDF

def txt_to_pdf(filename):
    # save FPDF() class into
    # a variable pdf
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=15)

    f = open(filename + ".txt", "r")

    # insert the texts in pdf
    for x in f:
        pdf.cell(200, 10, txt=x, ln=1, align='C')

    pdf.output(filename + ".pdf")
    f.close()


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
    filename = 'week' + str(consts.WEEK()) + 'results'
    with open(filename + ".txt", 'w') as f:
        f.write(league_name())
        f.write('\n')
        f.write("*************************")
        f.write('\n')
        f.write(league_owners())
        f.write('\n')
        f.write("*************************")
        f.write('\n')
        f.write("Week " + str(consts.WEEK()))
        f.write('\n')
        f.write("*************************")
        f.write('\n')
        f.write('\n'.join(matchup_results(matchups())))
    txt_to_pdf(filename)
