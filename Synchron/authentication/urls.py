from django.urls import path

from . import views

urlpatterns = [
    path("signup", views.CreateUser.as_view(), name="Sing Up"),
    path("signin", views.SignIn.as_view(), name="Sign In"),
    path("logout", views.Logout.as_view(), name="Logout"),
    path("user_info", views.User_Info.as_view(), name="User Info"),
]
