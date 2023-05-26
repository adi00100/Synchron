from rest_framework.response import Response


def is_logged_out(func):
    def wrapper(obj, request, *args, **kwargs):
        if request.custom_user:
            response = Response(
                {"msg": "User logged in."},
            )
            response["Location"] = "/"
            response.status_code = 302
            return response

        return func(obj, request, *args, **kwargs)

    return wrapper
