from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="testland"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        driver = Driver.objects.create(
            username="testDriver",
            first_name="John",
            last_name="Smith",
            license_number="ABC12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="testland"
        )
        car = Car.objects.create(
            model="testmodel",
            manufacturer=manufacturer
        )
        self.assertEqual(
            str(car),
            f"{car.model}"
        )

