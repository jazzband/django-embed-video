from mock import patch
from unittest import TestCase

from django.forms import ValidationError

from ..fields import EmbedVideoField, EmbedVideoFormField
from ..backends import UnknownBackendException, UnknownIdException


class EmbedVideoFieldTestCase(TestCase):
    def setUp(self):
        self.field = EmbedVideoField()

    def test_formfield_form_class(self):
        self.assertIsInstance(self.field.formfield(),
                              EmbedVideoFormField)

    def test_south(self):
        self.assertEqual(self.field.south_field_triple(),
                         (
                             'embed_video.fields.EmbedVideoField',
                             [], {'max_length': '200'}
                         ))


class EmbedVideoFormFieldTestCase(TestCase):
    def setUp(self):
        self.formfield = EmbedVideoFormField()

    def test_validation_unknownbackend(self):
        with patch('embed_video.fields.detect_backend') as mock_detect_backend:
            mock_detect_backend.return_value = True
            mock_detect_backend.side_effect = UnknownBackendException
            self.assertRaises(ValidationError, self.formfield.validate,
                              ('http://youtube.com/v/123/',))

    def test_validation_unknownid(self):
        with patch('embed_video.fields.detect_backend') as mock_detect_backend:
            mock_detect_backend.return_value = True
            mock_detect_backend.side_effect = UnknownIdException
            self.assertRaises(ValidationError, self.formfield.validate,
                              ('http://youtube.com/v/123/',))

    def test_validation_correct(self):
        url = 'http://my-testing.url.com'
        with patch('embed_video.fields.detect_backend') as mock_detect_backend:
            mock_detect_backend.return_value = True
            self.assertEqual(url, self.formfield.validate(url))

    def test_validation_super(self):
        self.assertRaises(ValidationError, self.formfield.validate, '')

    def test_validation_allowed_empty(self):
        formfield = EmbedVideoFormField(required=False)
        self.assertIsNone(formfield.validate(''))
