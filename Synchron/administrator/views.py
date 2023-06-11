from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import status
from rest_framework.permissions import BasePermission
from utils import cursor
from utils.permission import role
from rest_framework.response import Response
from .models import Position, Team, Member
from rest_framework import parsers, status
from .serializers import (
    User_Retrieve_Serializer,
    Position_Create_Serializer,
    Position_Retrieve_Update_Serializer,
    Team_Create_Serializer,
    Team_Retrieve_Update_Serializer,
    Members_Create_Serializer,
)

from django.db.utils import IntegrityError

# Create your views here.
# Get all users
# Get scrum masters
# Get all positions and Add positions
# Get teams and create teams


class Retrieve_User(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = User_Retrieve_Serializer
    permission_classes = [role("admin")]

    def get(self, request):
        """
        ### List all users in the database.
        """
        cursor.execute("SELECT id,fname,lname from users")
        users = [{"id": i[0], "fname": i[1], "lname": i[2]} for i in cursor.fetchall()]
        response = Response(users, status=200)
        return response


class Retrieve_Scrum_Master(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = User_Retrieve_Serializer
    permission_classes = [role("admin")]

    def get(self, request):
        """
        ### List all scrum masters among users so that they can be assigned to the team.
        """
        cursor.execute("SELECT id,fname,lname from users where role='SM';")
        users = [{"id": i[0], "fname": i[1], "lname": i[2]} for i in cursor.fetchall()]
        response = Response({"users": users}, status=200)
        return response


class Positions(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    permission_classes = [role("admin")]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return Position_Create_Serializer
        elif self.request.method == "GET":
            return Position_Retrieve_Update_Serializer

    def post(self, request):
        """
        ### Create positions such as Frontend,Backend,QA,etc.
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            position = Position(name=data["name"])

            try:
                id = position.insert()
                return Response({"id": position.id, "name": position.name}, status=200)
            except IntegrityError:
                return Response(
                    {"msg": "Position already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response({"msg": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        ### List all positions available.
        """
        cursor.execute("SELECT id,name FROM positions;")
        positions = [{"id": i[0], "name": i[1]} for i in cursor.fetchall()]
        return Response({"positions": positions}, status=200)


class Teams(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    permission_classes = [role("admin")]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return Team_Create_Serializer
        elif self.request.method == "GET":
            return Team_Retrieve_Update_Serializer

    def post(self, request):
        """
        ### Create a team and assign the scrum master.
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            team = Team(name=data["name"], scrum_master=data["scrum_master"])
            try:
                cursor.execute(
                    f"SELECT 1 FROM USERS WHERE id='{team.scrum_master}' and role='SM'"
                )

                if cursor.fetchall():
                    id = team.insert()
                    return Response({"id": id}, status=200)
                else:
                    return Response(
                        {"msg": "User not a scrum master."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except IntegrityError:
                return Response(
                    {"msg": "Team already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except:
                return Response(
                    {"msg": "Couldn't Create team"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response({"msg": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        ### List all teams  in the database.
        """
        cursor.execute("SELECT * FROM TEAMS")
        res = [
            {"id": i[0], "name": i[1], "scrum_master": i[2]} for i in cursor.fetchall()
        ]
        return Response(res, status=200)


class Add_Members(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = Members_Create_Serializer
    permission_classes = [role("admin")]

    def post(self, request):
        """
        ### Add members to the team.
        - poistion_id and member_id are supposed to be array.
        - member_id[i] would have the position position_id[i].
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            success = []
            err = []
            for m in data["members"]:
                member = Member(
                    team_id=data["team_id"],
                    member_id=m["member_id"],
                    position=m["position"],
                )
                try:
                    member.insert()
                    success.append(member.member_id)
                except:
                    err.append(member.member_id)

            return Response({"success": success, "error": err}, status=200)
        return Response({"msg": "invalid data."}, status=status.HTTP_400_BAD_REQUEST)


class Retrieve_Member(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = User_Retrieve_Serializer
    permission_classes = [role("admin")]

    def get(self, request, team_id):
        """
        ### List all the members of the team.
        """

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

        members = [
            {"id": i[0], "fname": i[1], "lname": i[2], "role": i[3], "position": i[4]}
            for i in cursor.fetchall()
        ]
        return Response(members, status=200)
