from unittest import TestCase
from unittest.mock import patch

from django.forms import ValidationError

from ..fields import EmbedVideoField, EmbedVideoFormField
from ..backends import UnknownBackendException, UnknownIdException, YoutubeBackend


class EmbedVideoFieldTestCase(TestCase):
    def setUp(self):
        self.field = EmbedVideoField()

    def test_formfield_form_class(self):
        self.assertIsInstance(self.field.formfield(), EmbedVideoFormField)


class EmbedVideoFormFieldTestCase(TestCase):
    def setUp(self):
        self.formfield = EmbedVideoFormField()

    def test_validation_unknown_backend(self):
        with patch("embed_video.fields.detect_backend") as mock_detect_backend:
            mock_detect_backend.return_value = True
            mock_detect_backend.side_effect = UnknownBackendException
            self.assertRaises(
                ValidationError, self.formfield.validate, ("http://youtube.com/v/123/",)
            )

    def test_validation_unknown_id(self):
        with patch("embed_video.fields.detect_backend") as mock_detect_backend:
            mock_detect_backend.return_value = True
            mock_detect_backend.side_effect = UnknownIdException
            self.assertRaises(
                ValidationError, self.formfield.validate, ("http://youtube.com/v/123/",)
            )

    def test_validation_correct(self):
        url = "http://www.youtube.com/watch?v=gauN0gzxTcU"
        with patch("embed_video.fields.detect_backend") as mock_detect_backend:
            mock_detect_backend.return_value = YoutubeBackend(url)
            self.assertEqual(url, self.formfield.validate(url))

    def test_validation_unknown_code(self):
        url = "http://www.youtube.com/edit?abcd=abcd"
        self.assertRaises(ValidationError, self.formfield.validate, url)

    def test_validation_super(self):
        self.assertRaises(ValidationError, self.formfield.validate, "")

    def test_validation_allowed_empty(self):
        formfield = EmbedVideoFormField(required=False)
        self.assertIsNone(formfield.validate(""))
