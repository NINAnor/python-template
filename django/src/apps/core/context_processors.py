from django.conf import settings
from django.http import HttpRequest
from django.template import Context


def context_settings(request: HttpRequest) -> Context:
    return {
        "PROJECT_NAME": settings.PROJECT_NAME,
    }
