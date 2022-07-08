from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from taxi.models import Manufacturer, Driver, Car
from taxi.views import car_assign

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
# DRIVER_DETAIL_URL = reverse("taxi:driver-detail")
CAR_URL = reverse("taxi:car-list")
# CAR_DETAIL_URL = reverse("taxi:car-detail")



class PublicTests(TestCase):
    def test_manufacturer_login_required(self):
        result = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_driver_login_required(self):
        result = self.client.get(DRIVER_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_car_login_required(self):
        result = self.client.get(CAR_URL)
        self.assertNotEqual(result.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "name",
            "password1234",
            license_number="QDE12345"
        )
        self.client.force_login(self.user)

    def test_get_manufacturers(self):
        Manufacturer.objects.create(name="test_name", country="testland")
        Manufacturer.objects.create(name="test_name1", country="testland1")

        response = self.client.get(MANUFACTURER_URL)
        all_manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(all_manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_get_cars(self):
        manufacturer = Manufacturer.objects.create(name="test_name", country="testland")
        Car.objects.create(model="test_name", manufacturer=manufacturer)
        Car.objects.create(model="test_name1", manufacturer=manufacturer)

        response = self.client.get(CAR_URL)
        all_cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["cars_list"]),
            list(all_cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_get_drivers(self):
        Driver.objects.create(username="testname", first_name="test_first",
                              last_name="test_second", license_number="ABC12345")

        response = self.client.get(DRIVER_URL)
        all_drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(
            list(response.context["drivers_list"]),
            list(all_drivers)
        )

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "newuser12345pass",
            "password2": "newuser12345pass",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "DKT11112"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_car_assign(self):
        manufacturer = Manufacturer.objects.create(name="test_name", country="testland")
        test_car = Car.objects.create(model="test_name", manufacturer=manufacturer)

        car_assign(self, test_car.pk)
        self.assertEqual(list(test_car.drivers.all()), [self.user])

        car_assign(self, test_car.pk)
        self.assertEqual(list(test_car.drivers.all()), [])




