from utils import cursor
from utils.descriptor import ID, Name
from django.db import connection


class Team:
    __table_name__ = "teams"
    __fields_str__ = "id,name,scrum_master"
    __fields__ = tuple(__fields_str__.split(","))
    id: str = ID()
    name: str = Name()
    scrum_master: str

    def __init__(self, name, scrum_master, id=None) -> None:
        self.id = id
        self.name = name
        self.scrum_master = scrum_master

    def insert(self):
        query = f"""
            INSERT INTO {self.__table_name__}({self.__fields_str__})
            VALUES('{self.id}','{self.name}','{self.scrum_master}')
        """
        with connection.cursor() as cursor:
            cursor.execute(query)

        return self.id


class Position:
    __table_name__ = "positions"
    __fields_str__ = "id,name"
    __fields__ = tuple(__fields_str__.split(","))
    id: str = ID()
    name: str = Name()

    def __init__(self, name, id=None) -> None:
        self.name = name
        self.id = id

    def insert(self):
        query = f"""
            INSERT INTO {self.__table_name__}({self.__fields_str__})
            VALUES('{self.id}','{self.name}')
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
        return self.id


class Member:
    __table_name__ = "members"
    __fields_str__ = "id,team_id,member_id,position"
    __fields__ = tuple(__fields_str__.split(","))
    id: str = ID()
    team_id: str
    member_id: str
    position: str

    def __init__(self, team_id, member_id, position, id=None) -> None:
        self.id = id
        self.team_id = team_id
        self.member_id = member_id
        self.position = position

    def insert(self):
        query = f"""
            INSERT INTO {self.__table_name__}({self.__fields_str__})
            VALUES('{self.id}','{self.team_id}','{self.member_id}','{self.position}')
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
        return self.id
