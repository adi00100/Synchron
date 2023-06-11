from rest_framework import serializers


class Serializer(serializers.Serializer):
    pass


class SignIn_Serializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class SignUp_Serializer(SignIn_Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.CharField()


class Info_Serializer(Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.CharField()
    email = serializers.EmailField()
