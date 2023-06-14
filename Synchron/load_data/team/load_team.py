from utils import cursor
from administrator.models import Team
import random


def get_sm():
    sm = []
    data = open("./load_data/user/loaded_user_data.csv").readlines()
    for i in data:
        i = i.rstrip().split(",")
        if i[-1] == "SM":
            sm.append(i[0])

    return sm


def run():
    sm = get_sm()

    cursor.execute("TRUNCATE TABLE TEAMS CASCADE")

    data = open(f"./load_data/team/team_data.csv", "r").readlines()
    data = data[1:]
    loaded_data = open(f"./load_data/team/loaded_team_data.csv", "w")
    loaded_data.write("id,name,scrum master\n")
    for i, j in zip(data, sm):
        i = i.rstrip().split(",")
        id = Team(name=i[0], scrum_master=j).insert()
        i.insert(0, id)
        i.append(j)
        loaded_data.write(",".join(i) + "\n")
