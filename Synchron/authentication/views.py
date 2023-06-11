from rest_framework import parsers, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import User
from .serializers import (
    SignIn_Serializer,
    SignUp_Serializer,
    Serializer,
    Info_Serializer,
)
from django.db.utils import IntegrityError
from .sessions import Session
from .decorators import is_logged_out
from utils.permission import IsAuthenticated, IsNotAuthenticated


class SignIn(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = SignIn_Serializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        """
        ### End point to sign in a user. Uses cookie to set cookie in the browser.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.get_by_email(data["email"])
            if user:
                if user.check_password(data["password"]):
                    session = Session(user.id)
                    response = session.set_cookie_response()
                    return response

        return Response(
            {"msg": "Login unsuccessful."}, status=status.HTTP_400_BAD_REQUEST
        )


class CreateUser(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = SignUp_Serializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        """
        ### Create a user.
        - must be logged out.
        - email must be unique.
        """
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        ### Logout the user and clear the session cookies.
        """
        response = Session.delete_cookie_response(request.user_id, request.session_id)
        response.status_code = 302
        return response


class User_Info(GenericAPIView):
    parser_classes = (parsers.JSONParser,)
    serializer_class = Info_Serializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        ### Return the information about the currently signed in user.
        """
        response = {}
        if request.custom_user:
            response = {
                "first_name": request.custom_user.fname,
                "last_name": request.custom_user.lname,
                "email": request.custom_user.email,
                "role": request.custom_user.role,
            }

        return Response(response, status=200)
