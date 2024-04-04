from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from dronerental.rentalservice.models import Category

class CategoryAPITest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Surveillance", description="Drones for surveillance.")

    def test_create_category(self):
        """
        Ensure we can create a new category object.
        """
        url = reverse('category-list')
        data = {'name': 'Photography', 'description': 'Drones for photography.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(id=2).name, 'Photography')

    def test_get_category(self):
        """
        Ensure we can get a category object.
        """
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Surveillance')

    def test_update_category(self):
        """
        Ensure we can update a category object.
        """
        url = reverse('category-detail', args=[self.category.id])
        data = {'name': 'Updated Name', 'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Name')

    def test_delete_category(self):
        """
        Ensure we can delete a category object.
        """
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())
