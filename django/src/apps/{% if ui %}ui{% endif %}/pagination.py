import logging
import traceback
from typing import Self

from django.core.paginator import Paginator
from django.db import connection
from django.db.models.query import QuerySet
from django.utils.functional import cached_property


class EstimateWithoutFiltersPaginator(Paginator):
    """
    Combination of ideas from:
     - https://gist.github.com/safar/3bbf96678f3e479b6cb683083d35cb4d
     - https://medium.com/@hakibenita/optimizing-django-admin-paginator-53c4eb6bfca3
    Overrides the count method of QuerySet objects to avoid timeouts.
    - get an estimate instead of actual count when not filtered
      (this estimate can be stale and hence not fit for
    situations where the count of objects actually matter).
    - If any other exception occured fall back to default behaviour.
    """

    def __init__(self: Self, *args, qs: QuerySet = None, **kwargs) -> Self:
        """
        read additional qs parameter, look at FilterCompatibleTablePagination.paginate
        this is necessary because django_tables2.Table
        would pass an object that isn't a queryset
        """
        super().__init__(*args, **kwargs)
        self.qs = qs

    @cached_property
    def count(self: Self) -> int:
        """
        Returns an estimated number of objects, across all pages.
        """
        object_list = None

        if hasattr(self.object_list, "query"):
            object_list = self.object_list

        if hasattr(self.qs, "query"):
            object_list = self.qs

        try:
            """
            beware - don't try to test object_list, this would actually execute an
            under-performant query because the queryset are lazy evalueted
            just try to check and if somethings fail, just skip this
            """
            if not object_list.query.where:
                with connection.cursor() as cursor:
                    # Obtain estimated values (only valid with PostgreSQL)
                    # in case of negative number return 0
                    table_name = object_list.query.model._meta.db_table
                    cursor.execute(
                        "SELECT reltuples FROM pg_class WHERE relname = %s",
                        [table_name],
                    )
                    estimate = int(cursor.fetchone()[0])
                    if estimate < 0:
                        logging.warn(
                            f"{table_name} returned negative estimate {estimate},"
                            + " this may require VACUUM/ANALYZE such table",
                        )
                        return 0
                    return estimate
        except Exception:
            # If any other exception occurred fall back to default behaviour
            logging.warning(traceback.format_exc())

        return super().count


class FilterCompatibleTablePagination:
    def paginate(
        self: Self,
        per_page: int = None,
        page: int = 1,
        *args,
        paginator_class: Paginator = None,
        **kwargs,
    ) -> Self:
        per_page = per_page or self._meta.per_page
        """
        inject the original queryset inside the paginator,
        so that it can understand if any where is present
        self.data.data reads from Table data
        """
        self.paginator = EstimateWithoutFiltersPaginator(
            self.rows,
            per_page,
            *args,
            qs=self.data.data,
            **kwargs,
        )
        self.page = self.paginator.page(page)

        return self
