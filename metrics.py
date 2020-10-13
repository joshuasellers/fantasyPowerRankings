import requests
import consts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_request(p):
    league_id = 251025
    year = 2020
    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id)
    return requests.get(url, params=p, cookies={'SWID': consts.SWID(), 'espn_s2': consts.espn_s2()})


def get_games():
    params = {"view": "mMatchup"}
    r = get_request(params)
    d = r.json()

    df = [[
            game['matchupPeriodId'],
            game['home']['teamId'], game['home']['totalPoints'],
            game['away']['teamId'], game['away']['totalPoints']
        ] for game in d['schedule']]

    df = pd.DataFrame(df, columns=['Week', 'Team1', 'Score1', 'Team2', 'Score2'])
    df['Type'] = ['Regular' if w<=14 else 'Playoff' for w in df['Week']]
    return df


def get_avg():
    df = get_games()
    avgs = (df.filter(['Week', 'Score1', 'Score2'])
              .melt(id_vars=['Week'], value_name='Score')
              .groupby('Week')
              .mean()
              .reset_index())
    return avgs

