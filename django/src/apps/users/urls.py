from apps.users.views import (
    UserDetail,
    UsersList,
    UserUpdate,
    user_redirect_view,
    user_update_view,
)
from django.urls import path

app_name = "users"
urlpatterns = [
    path("", view=UsersList.as_view(), name="list"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=UserDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", view=UserUpdate.as_view(), name="edit"),
]
