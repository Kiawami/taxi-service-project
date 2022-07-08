from django.test import TestCase

from taxi.forms import DriverCreateForm


class FormTests(TestCase):
    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "newuser12345pass",
            "password2": "newuser12345pass",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "DKT11112"
        }
        form = DriverCreateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_validation(self):
        form_data = {
            "username": "new_user",
            "password1": "newuser12345pass",
            "password2": "newuser12345pass",
            "first_name": "first name",
            "last_name": "last name",
        }

        wrong_license_numbers = ["QWE1234", "QWE123456", "12312345",
                                 "qwe12345", "q1212345", "12345QWE"]

        for license_number in wrong_license_numbers:
            form_data["license_number"] = license_number
            form = DriverCreateForm(data=form_data)
            self.assertFalse(form.is_valid())

