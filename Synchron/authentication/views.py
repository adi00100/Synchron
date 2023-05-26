from rest_framework import parsers, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import User
from .serializers import SignIn_Serializer, SignUp_Serializer, Serializer
from django.db.utils import IntegrityError
from .sessions import Session
from .decorators import is_logged_out


class SignIn(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = SignIn_Serializer

    @is_logged_out
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.get_by_email(data["email"])
            if user:
                if user.check_password(data["password"]):
                    session = Session(user.id)
                    response = session.set_cookie_response()
                    response["Location"] = "/"
                    response.status_code = 302
                    return response

        return Response(
            {"msg": "Login unsuccessful."}, status=status.HTTP_400_BAD_REQUEST
        )


class CreateUser(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = SignUp_Serializer

    @is_logged_out
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User(
                email=data["email"],
                password=data["password"],
                lname=data["last_name"],
                fname=data["first_name"],
                role=data["role"],
            )
            try:
                user.insert()
            except IntegrityError:
                return Response(
                    {"msg": "Email already signed up."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response({"msg": "Signup successful."})


class Logout(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = Serializer

    def post(self, request):
        response = Session.delete_cookie_response(request.user_id, request.session)
        response["Location"] = "/"
        response.status_code = 302
        return response
