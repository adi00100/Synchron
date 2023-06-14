from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.db import connection


def role(name):
    class Role(BasePermission):
        exception = PermissionDenied(f"User is required to be {name}")

        def has_permission(self, request, view):
            try:
                if request.custom_user.role == name:
                    return True
                else:
                    raise self.exception
            except:
                raise self.exception

    return Role


class IsAuthenticated(BasePermission):
    exception = PermissionDenied(f"User not authenticated.")

    def has_permission(self, request, view):
        try:
            if request.custom_user:
                return True
            else:
                raise self.exception
        except:
            raise self.exception


class IsNotAuthenticated(BasePermission):
    exception = PermissionDenied(f"User needs to logout.")

    def has_permission(self, request, view):
        try:
            if not bool(request.custom_user):
                return True
            else:
                raise self.exception
        except:
            raise self.exception


class BelongsToTeam(BasePermission):
    exception = PermissionDenied(f"User does not belong to this team.")

    def has_permission(self, request, view):
        try:
            team_id = view.kwargs["team_id"]
            cursor = connection.cursor()

            cursor.execute(
                f"""
                    SELECT 1 FROM members WHERE team_id='{team_id}' AND member_id='{request.custom_user.id}'
                    UNION
                    SELECT 1 FROM teams WHERE id='{team_id}' AND scrum_master='{request.custom_user.id}'
                """
            )
            if bool(cursor.fetchone()):
                return True
            else:
                raise self.exception
        except:
            raise self.exception


class CanAccessCard(BasePermission):
    exception = PermissionDenied(f"User can't access this card.")

    def has_permission(self, request, view):
        try:
            card_id = view.kwargs["card_id"]
            cursor = connection.cursor()

            cursor.execute(
                f"""
                        SELECT * FROM
                        (
                                SELECT scrum_master AS id
                                FROM teams JOIN stand_up_cards ON teams.id=stand_up_cards.team_id
                                WHERE stand_up_cards.id='{card_id}'

                                UNION

                                SELECT members.member_id AS id
                                FROM members JOIN stand_up_cards ON members.team_id=stand_up_cards.team_id
                                WHERE stand_up_cards.id='{card_id}'
                        ) AS a
                    WHERE  id='{request.custom_user.id}'
                """
            )
            if bool(cursor.fetchone()):
                return True
            else:
                raise self.exception

        except:
            raise self.exception


class CanChangeStandUp(BasePermission):
    exception = PermissionDenied(f"User cant modify or craete this card.")

    def has_permission(self, request, view):
        try:
            team_id = request.data["team_id"]
            cursor = connection.cursor()

            cursor.execute(
                f"""
                    SELECT 1 FROM teams WHERE id='{team_id}' AND scrum_master='{request.custom_user.id}'
                """
            )
            if bool(cursor.fetchone()):
                return True
            else:
                raise self.exception

        except:
            raise self.exception
