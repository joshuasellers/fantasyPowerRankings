import requests
import consts

scores = {}
league_id = 251025
year = 2020
url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2020/segments/0/leagues/251025"

r = requests.get(url, cookies={'SWID': consts.SWID(), 'espn_s2': consts.espn_s2()})

d = r.json()

print(d)

