from django import template
from slippers.templatetags.slippers import register_components

register = template.Library()
register_components(
    {
        "fa_icon": "ui/components/fa_icon.html",
    },
    register,
)
