from utils import cursor
from authentication.models import User


def run():
    cursor.execute("TRUNCATE TABLE USERS CASCADE")

    data = open(f"./load_data/user/user_data.csv", "r").readlines()
    header, data = data[0], data[1:]

    loaded_data = open(f"./load_data/user/loaded_user_data.csv", "w")
    loaded_data.write("id," + header)
    for i in data:
        i = i.rstrip().split(",")
        id = User(fname=i[0], lname=i[1], email=i[2], password=i[3], role=i[4]).insert()
        i.insert(0, id)
        loaded_data.write(",".join(i) + "\n")
