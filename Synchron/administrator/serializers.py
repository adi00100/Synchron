from rest_framework import serializers


class Serializer(serializers.Serializer):
    pass


class With_Id(Serializer):
    id = serializers.CharField()


class User_Retrieve_Serializer(With_Id):
    fname = serializers.CharField()
    lname = serializers.CharField()


class Team_Create_Serializer(Serializer):
    name = serializers.CharField()
    scrum_master = serializers.CharField()


class Team_Retrieve_Update_Serializer(With_Id, Team_Create_Serializer):
    pass


class Position_Create_Serializer(Serializer):
    name = serializers.CharField()


class Position_Retrieve_Update_Serializer(With_Id, Position_Create_Serializer):
    pass


class Member_Create_Serializer(Serializer):
    member_id = serializers.CharField()
    position = serializers.CharField()


class Members_Create_Serializer(Serializer):
    team_id = serializers.CharField()
    members = serializers.ListField(child=Member_Create_Serializer())


class Member_Retrieve_Update_Serializer(With_Id, Members_Create_Serializer):
    pass
