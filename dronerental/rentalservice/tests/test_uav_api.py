from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from dronerental.rentalservice.models import UAV, Brand, Category

class UAVAPITest(APITestCase):

    def setUp(self):
        # Create instances of Brand and Category for the foreign keys required by UAV
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

    def test_create_uav(self):
        """
        Ensure we can create a new UAV object.
        """
        url = reverse('uav-list')
        data = {
            'name': 'Mavic 2 Pro',
            'description': 'Compact and powerful drone.',
            'brand': self.brand.id,
            'category': self.category.id,
            'availability': True,
            'camera_quality': '4K',
            'max_payload': 0.9,
            'range': 8,
            'weight': 0.9,
            'endurance': 31,
            'operating_conditions': 'Daytime, clear weather',
            'night_flight_capable': True
        }
        response = self.client.post(url, data, format='json')
        # log the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UAV.objects.count(), 2)

    def test_get_uav(self):
        """
        Ensure we can get a UAV object.
        """
        url = reverse('uav-detail', args=[self.uav.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Phantom 4')

    def test_update_uav(self):
        """
        Ensure we can update a UAV object.
        """
        url = reverse('uav-detail', args=[self.uav.id])
        data = {
            'name': 'Phantom 4 Pro V2.0',
            'description': self.uav.description,  # Keeping other fields the same for simplicity
            'brand': self.brand.id,
            'category': self.category.id,
            'availability': self.uav.availability,
            'camera_quality': self.uav.camera_quality,
            'max_payload': self.uav.max_payload,
            'range': self.uav.range,
            'endurance': self.uav.endurance,
            'weight': self.uav.weight,
            'operating_conditions': self.uav.operating_conditions,
            'night_flight_capable': self.uav.night_flight_capable
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.uav.refresh_from_db()
        self.assertEqual(self.uav.name, 'Phantom 4 Pro V2.0')

    def test_delete_uav(self):
        """
        Ensure we can delete a UAV object.
        """
        url = reverse('uav-detail', args=[self.uav.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UAV.objects.filter(id=self.uav.id).exists())
