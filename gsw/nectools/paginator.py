import inspect

from django.core.paginator import Paginator
from django.db import connection
from django.utils.functional import cached_property
from django.utils.inspect import method_has_no_args


class LargeTablePaginator(Paginator):
    """
    ATENÇÃO: Funciona somente com Postgresql
    Warning: Postgresql only hack
    Overrides the count method of QuerySet objects to get an estimate instead of actual count when not filtered.
    However, this estimate can be stale and hence not fit for situations where the count of objects actually matter.
    """

    def _get_count(self):
        count_method = getattr(self.object_list, 'count', None)
        if callable(count_method) and not inspect.isbuiltin(count_method) and method_has_no_args(count_method):
            return count_method()
        return len(self.object_list)

    @cached_property
    def count(self):
        query = self.object_list.query
        if not query.where:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT reltuples FROM pg_class WHERE relname = %s",
                               [query.model._meta.db_table])
                return int(cursor.fetchone()[0])
            except Exception:
                return self._get_count()
        return self._get_count()
