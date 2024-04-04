from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from dronerental.rentalservice.models import Brand

class BrandAPITest(APITestCase):

    def setUp(self):
        self.brand = Brand.objects.create(name="DJI", description="Leading in civilian drones and aerial imaging technology.")

    def test_create_brand(self):
        """
        Ensure we can create a new brand object.
        """
        url = reverse('brand-list')
        data = {'name': 'Parrot', 'description': 'Innovative drones for all purposes.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Brand.objects.count(), 2)
        self.assertEqual(Brand.objects.get(id=2).name, 'Parrot')

    def test_get_brand(self):
        """
        Ensure we can get a brand object.
        """
        url = reverse('brand-detail', args=[self.brand.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'DJI')

    def test_update_brand(self):
        """
        Ensure we can update a brand object.
        """
        url = reverse('brand-detail', args=[self.brand.id])
        data = {'name': 'DJI Updated', 'description': 'Leading and evolving in drone technology.'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.brand.refresh_from_db()
        self.assertEqual(self.brand.name, 'DJI Updated')

    def test_delete_brand(self):
        """
        Ensure we can delete a brand object.
        """
        url = reverse('brand-detail', args=[self.brand.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Brand.objects.filter(id=self.brand.id).exists())
