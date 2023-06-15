import json
from utils.permission import role
from rest_framework.generics import GenericAPIView
from rest_framework import parsers, status
from rest_framework.response import Response
from utils import cursor
from utils.permission import (
    IsAuthenticated,
    BelongsToTeam,
    CanAccessCard,
    CanChangeStandUp,
)
from .models import Stand_Up_Cards, Remarks
from .serializers import (
    Team_Retrieve_Serializer,
    Member_Serializer,
    StandUp_Retrieve_Serializer,
    StandUp_Create_Serializer,
    StandUp_Summary_Retrieve_Serializer,
    StandUp_Update_Serializer,
)
from django.db import connection

# List all teams/standup board user is involved
# Open and view the team members
# Scrum Master can create/update the standup cards.
# Any user in the team can view all standup cards


class Teams_View(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = Team_Retrieve_Serializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        #### Get the list of teams in which the user is invlove.
        """
        with connection.cursor() as cursor:
            if request.custom_user.role == "SM":
                cursor.execute(
                    f"SELECT teams.id,teams.name FROM teams where scrum_master='{request.custom_user.id}'"
                )
            else:
                cursor.execute(
                    f"SELECT teams.id,teams.name FROM members JOIN teams on members.team_id=teams.id where members.member_id='{request.custom_user.id}'"
                )

            teams = [{"id": i[0], "name": i[1]} for i in cursor.fetchall()]

        return Response(teams, status=200)


class Members_View(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = Member_Serializer
    permission_classes = [BelongsToTeam]

    def get(self, request, team_id):
        """
        #### Get the list of members of the given team if the user is involved in it.
        """
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT users.id,users.fname,users.lname,users.role,result.position
                    FROM
                    (
                        (SELECT scrum_master AS id,NULL AS position FROM teams where id='{team_id}')
                        UNION
                        (SELECT members.member_id AS id,positions.name AS position FROM members JOIN positions ON members.position=positions.id WHERE members.team_id='{team_id}')
                    ) AS result
                    NATURAL JOIN
                    USERS 
                """
            )

            res = [
                {
                    "id": i[0],
                    "fname": i[1],
                    "lname": i[2],
                    "role": i[3],
                    "position": i[4],
                }
                for i in cursor.fetchall()
            ]

        return Response(res, status=200)


class StandUp(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    permission_classes = [CanChangeStandUp & role("SM")]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StandUp_Create_Serializer
        elif self.request.method == "PUT":
            return StandUp_Update_Serializer

    def post(self, request):
        """
        #### Create standup cards as a scrum master.
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                card = Stand_Up_Cards(
                    team_id=data["team_id"],
                    extra_notes=data["extra_notes"],
                    release_cycle=data["release_cycle"],
                    sprint_id=data["sprint_id"],
                    accomplished=data["accomplished"],
                    working_on=data["working_on"],
                    blockers=data["blockers"],
                )
                id = card.insert()
            except:
                return Response(
                    {"msg": "Card already exists for today."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT member_id from members where team_id='{card.team_id}'
                """
                )

                for i in cursor.fetchall():
                    remarks = Remarks(card_id=id, member_id=i[0], notes=[])
                    remarks.insert()

            return Response({"msg": "Card created", "id": id}, status=200)

        return Response({"msg": "invalid data."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        #### Update remarks or the standup card.
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        UPDATE stand_up_cards SET 
                        release_cycle='{data["release_cycle"]}',sprint_id='{data["sprint_id"]}',extra_notes='{data["extra_notes"]}',accomplished='{data["accomplished"]}',working_on='{data["working_on"]}',blockers='{data["blockers"]}'
                        WHERE id='{data["id"]}'
                    """
                )

                for i in data["remarks"]:
                    cursor.execute(
                        f"""UPDATE remarks SET notes='{json.dumps(i["notes"])}' WHERE id='{i["id"]}'"""
                    )

            return Response({"msg": "Data updated successfully."})
        return Response({"msg": "invalid data."}, status=status.HTTP_400_BAD_REQUEST)


class StandUp_Retrieve(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = StandUp_Summary_Retrieve_Serializer
    permission_classes = [BelongsToTeam]

    def get(self, request, team_id):
        """
        ### Get the list of standup cards for the given team.
        """
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM stand_up_cards where team_id='{team_id}' ORDER BY date DESC"
            )
            description = [
                cursor.description[i][0] for i in range(len(cursor.description))
            ]
            stand_up_cards = [dict(zip(description, i)) for i in cursor.fetchall()]

        return Response(stand_up_cards, status=200)


class Card_Retrieve(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = StandUp_Retrieve_Serializer
    permission_classes = [CanAccessCard]

    def get(self, request, card_id):
        """
        #### Get the details of the card.
        """
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM stand_up_cards where id='{card_id}'")
            description = [
                cursor.description[i][0] for i in range(len(cursor.description))
            ]
            stand_up_card = dict(zip(description, cursor.fetchone()))

            cursor.execute(
                f"""SELECT remarks.id AS id,users.fname AS fname, users.lname AS lname, remarks.notes AS notes,positions.name as position
                    FROM remarks
                    JOIN users ON remarks.member_id = users.id
                    JOIN stand_up_cards ON stand_up_cards.id = remarks.card_id
                    JOIN members ON members.member_id=users.id AND members.team_id=stand_up_cards.team_id
                    JOIN positions ON positions.id=members.position
                    WHERE remarks.card_id = '{card_id}'
                """
            )
            description = [
                cursor.description[i][0] for i in range(len(cursor.description))
            ]
            remarks = [dict(zip(description, i)) for i in cursor.fetchall()]
        for i in remarks:
            i["notes"] = json.loads(i["notes"])
        stand_up_card["remarks"] = remarks
        return Response(stand_up_card, status=200)
