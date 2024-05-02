from django.urls import path

from .views import UITemplateView

app_name = "ui"
urlpatterns = [
    path(
        "dashboard/",
        view=UITemplateView.as_view(template_name="ui/base.html"),
        name="dashboard",
    ),
]
