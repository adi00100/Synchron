from .sessions import Session
from .models import User


def auth(get_response):
    def add_user(request, *args, **kwargs):
        request.custom_user = None
        cookies = request.COOKIES
        user_id, session = cookies.setdefault("user_id"), cookies.setdefault("session")
        if user_id and session:
            if Session.validate(user_id, session):
                request.custom_user = User.get_by_id(cookies["user_id"])
                request.user_id = user_id
                request.session = session
            else:
                return Session.delete_cookie_response(user_id, session)

        response = get_response(request, *args, **kwargs)
        return response

    return add_user
