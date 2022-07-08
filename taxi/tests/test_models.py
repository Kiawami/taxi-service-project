from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Test",
                                                   country="Testland")
        car = Car.objects.create(model="testmodel", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Test",
                                                   country="Testland")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create(username="testname",
                                       first_name="test",
                                       last_name="name",
                                       license_number="TES12345")
        self.assertEqual(str(driver),
                         f"{driver.username} ({driver.first_name} {driver.last_name})")

