from django.urls import path, re_path

from . import views


urlpatterns = [
    path("teams", views.Teams_View.as_view(), name="View teams"),
    path("members/<str:team_id>", views.Members_View.as_view(), name="View members"),
    path("standup/", views.StandUp.as_view(), name="Create standup card"),
    path(
        "standup/<str:team_id>",
        views.StandUp_Retrieve.as_view(),
        name="Get standup cards info",
    ),
    path(
        "standup/card/<str:card_id>",
        views.Card_Retrieve.as_view(),
        name="Get standup cards info",
    ),
]
