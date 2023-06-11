from django.urls import path, re_path

from . import views

urlpatterns = [
    path("list_users", views.Retrieve_User.as_view(), name="List Users"),
    path("scrum_masters", views.Retrieve_Scrum_Master.as_view(), name="Scrum Master"),
    path("positions", views.Positions.as_view(), name="Position"),
    path("teams", views.Teams.as_view(), name="Teams"),
    path("members", views.Add_Members.as_view(), name="Add Member"),
    path("members/<str:team_id>", views.Retrieve_Member.as_view(), name="Get Member"),
    # path("logout", views.Logout.as_view(), name="Logout"),
]
