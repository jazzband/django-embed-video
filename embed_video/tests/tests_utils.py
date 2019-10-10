from unittest import TestCase

from django.core.exceptions import ImproperlyConfigured

from embed_video.utils import import_by_path


class ModuleImportTestCase(TestCase):
    """
    Taken from Django:

    https://github.com/django/django/blob/master/tests/utils_tests/test_module_loading.py
    """

    def test_incorrect_path(self):
        self.assertRaises(ImproperlyConfigured, import_by_path, "wrongpath")

    def test_incorrect_classname(self):
        self.assertRaises(ImproperlyConfigured, import_by_path, "embed_video.foo")

    def test_import_by_path(self):
        cls = import_by_path("embed_video.utils.import_by_path")
        self.assertEqual(cls, import_by_path)

        # Test exceptions raised
        for path in ("no_dots_in_path", "unexistent.path", "utils_tests.unexistent"):
            self.assertRaises(ImproperlyConfigured, import_by_path, path)

        with self.assertRaises(ImproperlyConfigured) as cm:
            import_by_path("unexistent.module.path", error_prefix="Foo")
        self.assertTrue(str(cm.exception).startswith("Foo"))
