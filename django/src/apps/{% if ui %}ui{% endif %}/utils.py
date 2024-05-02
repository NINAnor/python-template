from django.contrib.admin.utils import NestedObjects
from django.db.models import Model
from django.utils.encoding import force_str
from django.utils.text import capfirst


# https://stackoverflow.com/questions/12158714/how-to-show-related-items-using-deleteview-in-django
def get_deleted_objects(objs: list[Model]) -> tuple[list[Model], int, list[Model]]:
    collector = NestedObjects(using="default")
    collector.collect(objs)

    def format_callback(obj: Model) -> str:
        opts = obj._meta
        no_edit_link = f"{capfirst(opts.verbose_name)}: {force_str(obj)}"
        return no_edit_link

    to_delete = collector.nested(format_callback)
    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {
        model._meta.verbose_name_plural: len(objs)
        for model, objs in collector.model_objs.items()
    }
    return to_delete, model_count, protected
