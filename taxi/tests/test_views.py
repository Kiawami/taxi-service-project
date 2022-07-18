from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car
from taxi.views import car_assign

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


class LoginRequiredTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_manufacturer_login_required(self):
        result = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(result.status_code, 200)

    def test_car_login_required(self):
        result = self.client.get(CARS_URL)

        self.assertNotEqual(result.status_code, 200)

    def test_driver_login_required(self):
        result = self.client.get(DRIVERS_URL)

        self.assertNotEqual(result.status_code, 200)


class PrivateAccessTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_user",
            "password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        Manufacturer.objects.create(
            name="BMW", country="Germany"
        )

        result = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            list(result.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(result, "taxi/manufacturer_list.html")

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        Car.objects.create(
            model="first_car",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="second_car",
            manufacturer=manufacturer
        )

        result = self.client.get(CARS_URL)

        cars = Car.objects.all()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            list(result.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(result, "taxi/car_list.html")

    def test_retrieve_driver(self):
        Driver.objects.create_user(
            username="test_user1",
            password="testpassword654321",
            first_name="Test1",
            last_name="User1",
            license_number="CBA54321"
        )

        result = self.client.get(DRIVERS_URL)

        drivers = Driver.objects.all()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            list(result.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(result, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "testpassword12345",
            "password2": "testpassword12345",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "ABC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_assign_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        new_car = Car.objects.create(
            model="first_car",
            manufacturer=manufacturer
        )

        response = self.client.get(reverse("taxi:car-detail", args=["1"]))
        self.assertEqual(response.status_code, 200)

        car_assign(self, 1)
        self.assertEqual(
            list(self.user.cars.filter(id=1)),
            [new_car]
        )

        car_assign(self, 1)
        self.assertEqual(
            list(self.user.cars.filter(id=1)),
            []
        )

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        Car.objects.create(
            model="first_car",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="second_car",
            manufacturer=manufacturer
        )

        search_result = Car.objects.filter(model__icontains="firs")
        result_first = self.client.get(CARS_URL+"?model=firs")
        self.assertEqual(
            list(result_first.context["car_list"]),
            list(search_result)
        )

        search_result = Car.objects.filter(model__icontains="seco")
        result_second = self.client.get(CARS_URL + "?model=seco")
        self.assertEqual(
            list(result_second.context["car_list"]),
            list(search_result)
        )