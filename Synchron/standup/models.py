from utils import cursor
from utils.descriptor import Name, Email, Password, ID
from datetime import date
import json
from django.db import connection


class Remarks:
    __table_name__ = "remarks"
    __fields_str__ = "id,card_id,member_id,notes"
    __fields__ = tuple(__fields_str__.split(","))

    id = ID()
    card_id: str
    member_id: str
    notes: str

    def __init__(
        self, card_id: str, member_id: str, notes: str, id: str = None
    ) -> None:
        self.card_id = card_id
        self.member_id = member_id
        self.notes = notes
        self.id = id

    def insert(self):
        query = f"""
            INSERT INTO {self.__table_name__}({self.__fields_str__})
            VALUES('{self.id}','{self.card_id}','{self.member_id}','{json.dumps(self.notes)}')
        """
        with connection.cursor() as cursor:
            cursor.execute(query)

    @staticmethod
    def encode_notes(notes):
        """Notes will be in array encode to base64."""
        pass

    @staticmethod
    def decode_notes(notes):
        """Decode back to array."""
        pass


class Stand_Up_Cards:
    __table_name__ = "stand_up_cards"
    __fields_str__ = "id,team_id,date,release_cycle,sprint_id,extra_notes,accomplished,working_on,blockers"
    __fields__ = tuple(__fields_str__.split(","))

    id = ID()
    team_id: str
    date: str
    release_cycle: str
    sprint_id: str
    extra_notes: str
    accomplished: str
    working_on: str
    blockers: str

    def __init__(
        self,
        team_id: str,
        release_cycle: str,
        sprint_id: str,
        extra_notes: str,
        accomplished: str,
        working_on: str,
        blockers: str,
        id: str = None,
    ) -> None:
        self.id = id
        self.team_id = team_id
        self.date = date.today().strftime("%Y-%m-%d")
        self.release_cycle = release_cycle
        self.sprint_id = sprint_id
        self.extra_notes = extra_notes
        self.accomplished = accomplished
        self.working_on = working_on
        self.blockers = blockers

    def insert(self):
        query = f"""SELECT 1 FROM {self.__table_name__} WHERE team_id='{self.team_id}' and date='{self.date}'"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.fetchall():
                raise ValueError(
                    f"The standup card has already been created for the {self.date} for team {self.team_id}."
                )

            query = f"""
                INSERT INTO {self.__table_name__}({self.__fields_str__})
                VALUES('{self.id}','{self.team_id}','{self.date}','{self.release_cycle}','{self.sprint_id}','{self.extra_notes}','{self.accomplished}','{self.working_on}','{self.blockers}')
            """
            cursor.execute(query)
        return self.id
