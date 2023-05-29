from rest_framework.response import Response


def is_logged_out(func):
    def wrapper(obj, request, *args, **kwargs):
        print(f"from is_logged_out {request.custom_user}")
        if request.custom_user:
            response = Response(
                {"msg": "User logged in."},
            )
            response.status_code = 302
            return response

        return func(obj, request, *args, **kwargs)

    return wrapper
