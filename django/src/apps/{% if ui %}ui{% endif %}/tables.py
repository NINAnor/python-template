from typing import Any, Self

from django.utils.html import format_html
from django_tables2 import Column, Table


class UITable(Table):
    """
    Official table mixin, mostly used as base for the UI
    """

    extra = Column(verbose_name="Actions", empty_values=(), orderable=False)

    def __init__(self: Self, *args, show_total: bool = True, **kwargs) -> Self:  # noqa: ANN002
        super().__init__(*args, **kwargs)
        self._template = "ui/partials/table.html"
        self.show_total = show_total

    def render_extra(self: Self, value: Any, record: Any) -> str:  # noqa: ANN401
        return format_html(
            '<a href="{}"><i class="fas fa-edit"></i></a>',
            f"{record.id}/",
        )
