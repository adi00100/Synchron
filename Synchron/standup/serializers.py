from rest_framework import serializers
from rest_framework.serializers import Serializer


class With_Id(Serializer):
    id = serializers.CharField()


class Member_Serializer(With_Id):
    fname = serializers.CharField()
    lname = serializers.CharField()
    role = serializers.CharField()
    position = serializers.CharField()


class Team_Retrieve_Serializer(With_Id):
    name = serializers.CharField()


class Remarks_Create_Serialzer(Serializer):
    member_id = serializers.CharField()
    notes = serializers.ListField(child=serializers.CharField())


class Remarks_Retrieve_Update_Serializer(With_Id, Remarks_Create_Serialzer):
    pass


class StandUp_Create_Serializer(Serializer):
    team_id = serializers.CharField()
    release_cycle = serializers.CharField()
    sprint_id = serializers.CharField()
    extra_notes = serializers.CharField()
    accomplished = serializers.CharField()
    working_on = serializers.CharField()
    blockers = serializers.CharField()


class StandUp_Retrieve_Serializer(With_Id, StandUp_Create_Serializer):
    remarks = serializers.ListField(child=Remarks_Retrieve_Update_Serializer())


class Remarks_Update_Serializer(With_Id):
    notes = serializers.ListField(child=serializers.CharField())


class StandUp_Update_Serializer(With_Id):
    release_cycle = serializers.CharField()
    sprint_id = serializers.CharField()
    extra_notes = serializers.CharField()
    accomplished = serializers.CharField()
    working_on = serializers.CharField()
    blockers = serializers.CharField()
    remarks = serializers.ListField(child=Remarks_Update_Serializer())


class StandUp_Summary_Retrieve_Serializer(Serializer):
    team_id = serializers.CharField()
    release_cycle = serializers.CharField()
    sprint_id = serializers.CharField()
    extra_notes = serializers.CharField()
    accomplished = serializers.CharField()
    working_on = serializers.CharField()
    blockers = serializers.CharField()
