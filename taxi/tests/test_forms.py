from django.test import TestCase

from taxi.forms import DriverCreateForm
from taxi.models import Manufacturer, Driver, Car
from taxi.views import CarListView


class FormsTests(TestCase):
    def test_driver_creation(self):
        form_data = {
            "username": "new_user",
            "password1": "testpassword12345",
            "password2": "testpassword12345",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "ABC12345"
        }
        form = DriverCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_validation(self):
        form_data = {
            "username": "new_user",
            "password1": "testpassword12345",
            "password2": "testpassword12345",
            "first_name": "John",
            "last_name": "Smith",
        }

        wrong_license_numbers = ["12312345", "ABC1234",
                                 "ABC123456", "ABCD123",
                                 "AB123456", "aBc12345",
                                 "abc12345", "12345ABC"]

        for license_number in wrong_license_numbers:
            form_data["license_number"] = license_number
            form = DriverCreateForm(data=form_data)
            self.assertFalse(form.is_valid())

