from .sessions import Session
from .models import User
from rest_framework.response import Response


def auth(get_response):
    def add_user(request, *args, **kwargs):
        request.custom_user = None
        cookies = request.COOKIES
        request.user_id = cookies.setdefault("user_id")
        request.session_id = cookies.setdefault("session_id")
        if request.user_id and request.session_id:
            if Session.validate(request.user_id, request.session_id):
                request.custom_user = User.get_by_id(request.user_id)
            else:
                response = Session.delete_cookie_response(
                    request.user_id, request.session_id
                )
                request.user_id = None
                request.session_id = None
                return response
        response = get_response(request, *args, **kwargs)
        return response

    return add_user
