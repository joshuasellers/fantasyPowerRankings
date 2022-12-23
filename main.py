import json
import requests
import consts

def user_name(userid):
    response = requests.get("https://api.sleeper.app/v1/user/" + userid)
    json_response = json.loads(response.text)
    return consts.OWNER_NAMES()[json_response['username']]


def specific_league_rosters():
    response = requests.get("https://api.sleeper.app/v1/league/" + consts.LEAGUE_ID() + "/rosters")
    json_response = json.loads(response.text)
    for owner in json_response:
        print(user_name(owner['owner_id']))


if __name__ == '__main__':
    specific_league_rosters()
