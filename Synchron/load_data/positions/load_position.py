from utils import cursor
from administrator.models import Position


def run():
    cursor.execute("TRUNCATE TABLE POSITIONS CASCADE")

    data = open(f"./load_data/positions/position_data.csv", "r").readlines()
    header, data = data[0], data[1:]

    loaded_data = open(f"./load_data/positions/loaded_position_data.csv", "w")
    loaded_data.write(header)
    for i in data:
        i = i.rstrip().split(",")
        id = Position(name=i[0]).insert()
        i.insert(0, id)
        loaded_data.write(",".join(i) + "\n")
