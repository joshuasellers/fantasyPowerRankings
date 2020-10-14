import os
import pandas as pd


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return ""


def give_ranking(week_number):
    print("Rankings for week ", week_number)
    path = find('rankings.csv', str(week_number) + '/')
    if path == "":
        num_teams = input("Number of teams: ")
        teams = [""] * int(num_teams)
        for i in range(0, int(num_teams)):
            teams[i] = input("Team number " + str(i))
        print(teams)
    else:
        df = pd.read_csv(path)
        print(df)

