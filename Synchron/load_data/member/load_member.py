from utils import cursor
from administrator.models import Member
import random


def get_team():
    data = open(f"./load_data/team/loaded_team_data.csv", "r").readlines()[1:]
    teams = []
    for i in data:
        i = i.rstrip().split(",")
        teams.append(i[0])
    return teams


def get_position():
    data = open(f"./load_data/positions/loaded_position_data.csv", "r").readlines()[1:]
    positions = []
    for i in data:
        i = i.rstrip().split(",")
        positions.append(i[0])
    return positions


def get_users():
    data = open(f"./load_data/user/loaded_user_data.csv", "r").readlines()[1:]
    users = {"SM": [], "DEV": [], "admin": []}
    for i in data:
        i = i.rstrip().split(",")
        users[i[-1]].append(i[0])

    return users


def add_members(team, members, positions):
    loaded_data = open(f"./load_data/member/loaded_member.csv", "a")
    for m, p in zip(members, positions):
        member = Member(team_id=team, member_id=m, position=p)
        id = member.insert()
        loaded_data.write(f"{id},{team},{m},{p}\n")
    loaded_data.close()


def run():
    cursor.execute("TRUNCATE TABLE MEMBERS CASCADE")

    loaded_data = open(f"./load_data/member/loaded_member.csv", "w")
    loaded_data.write("id,team_id,member_id,position\n")
    users = get_users()["DEV"]
    positions = get_position()
    teams = get_team()
    for team in teams:
        member = set()
        while len(member) < 5:
            member.update(member.union({random.choice(users) for _ in range(10)}))

        position = [random.choice(positions) for _ in range(len(member))]
        add_members(team, member, position)
