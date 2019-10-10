from importlib import import_module

from django.core.exceptions import ImproperlyConfigured


def import_by_path(dotted_path, error_prefix=""):
    """
    Import a dotted module path and return the attribute/class designated by
    the last name in the path. Raise ImproperlyConfigured if something goes
    wrong.

    .. warning::
        .. deprecated:: Django 1.6

        Function :py:func:`django.utils.module_loading.import_by_path` has
        been added in Django 1.6.

    :param dotted_path: Path to imported attribute or class
    :type dotted_path: str

    :return: imported attribute or class
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "%s%s doesn't look like a module path" % (error_prefix, dotted_path)
        )
    try:
        module = import_module(module_path)
    except ImportError as e:
        msg = '%sError importing module %s: "%s"' % (error_prefix, module_path, e)
        raise ImproperlyConfigured(msg)
    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise ImproperlyConfigured(
            '%sModule "%s" does not define a "%s" \
                                   attribute/class'
            % (error_prefix, module_path, class_name)
        )
    return attr
