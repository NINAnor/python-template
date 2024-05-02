from apps.ui.tables import UITable

from .models import User


class UserTable(UITable):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
        ]
