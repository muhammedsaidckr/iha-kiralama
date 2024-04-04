from django.test import TestCase
from dronerental.rentalservice.models import UAV, Brand, Category

class UAVModelTest(TestCase):

    def setUp(self):
        # Setup run before every test method.
        self.brand = Brand.objects.create(name="DJI", description="Leading in civilian drones and aerial imaging technology.")
        self.category = Category.objects.create(name="Aerial Photography", description="UAVs designed for aerial photography and videography.")
        self.uav = UAV.objects.create(
            name="Phantom 4",
            description="High precision aerial photography UAV.",
            brand=self.brand,
            category=self.category,
            availability=True,
            camera_quality="4K",
            max_payload=1.5,
            range=5,
            weight=1.4,
            endurance=30,
            operating_conditions="Daytime, clear weather",
            night_flight_capable=False
        )

    def test_uav_creation(self):
        """Test the UAV model can create a UAV."""
        self.assertEqual(self.uav.name, "Phantom 4")
        self.assertEqual(self.uav.description, "High precision aerial photography UAV.")
        self.assertTrue(self.uav.availability)

    def test_uav_update(self):
        """Test the UAV model can update a UAV's details."""
        self.uav.name = "Phantom 4 Pro"
        self.uav.save()
        updated_uav = UAV.objects.get(id=self.uav.id)
        self.assertEqual(updated_uav.name, "Phantom 4 Pro")

    def test_uav_delete(self):
        """Test the UAV model can delete a UAV."""
        uav_id = self.uav.id
        self.uav.delete()
        self.assertFalse(UAV.objects.filter(id=uav_id).exists())

    def test_uav_list(self):
        """Test the UAV model can list all UAVs."""
        UAV.objects.create(
            name="Mavic 2 Pro",
            description="Compact and powerful drone.",
            brand=self.brand,
            category=self.category,
            availability=True,
            camera_quality="4K",
            max_payload=0.9,
            range=8,
            endurance=31,
            weight=0.9,
            operating_conditions="Daytime, clear weather",
            night_flight_capable=True
        )
        self.assertEqual(UAV.objects.count(), 2)
