from slippers.templatetags.slippers import register_components

from django import template

register = template.Library()
register_components(
    {
        "fa_icon": "ui/components/fa_icon.html",
    },
    register,
)
