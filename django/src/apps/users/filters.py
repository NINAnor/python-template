from django_filters import FilterSet

from .models import User


class UserFilterSet(FilterSet):
    class Meta:
        model = User
        fields = [
            "email",
            "id",
        ]
