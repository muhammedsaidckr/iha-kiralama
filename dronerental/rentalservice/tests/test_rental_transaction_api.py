from datetime import timedelta, datetime

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from dronerental.rentalservice.models import User, UAV, Brand, Category, RentalTransaction


class RentalTransactionAPITests(APITestCase):

    def setUp(self):
        # Create instances of User and UAV for the foreign keys required by RentalTransaction
        self.user = User.objects.create(username='testuser', first_name='Test', last_name='User',
                                        password='testpass123')
        self.brand = Brand.objects.create(name="DJI", description="Leading in civilian drones and aerial imaging technology.")
        self.category = Category.objects.create(name="Aerial Photography", description="UAVs designed for aerial photography and videography.")
        self.uav = UAV.objects.create(
            name='Test UAV',
            description='Test description',
            hourly_rate=100,
            max_payload=5.0,
            range=500,
            endurance=120,
            weight=2.0,
            operating_conditions='Optimal',
            camera_quality='4K',
            night_flight_capable=True,
            brand=self.brand,
            category=self.category,
        )
        self.rental_transaction = RentalTransaction.objects.create(
            uav=self.uav,
            user=self.user,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(hours=2),
        )

    def test_create_rental_transaction(self):
        url = reverse('rentaltransaction-list')
        data = {
            'uav': self.uav.id,
            'user': self.user.id,
            'start_date': '2021-07-01T12:00:00Z',
            'end_date': '2021-07-01T14:00:00Z',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_rental_transaction(self):
        url = reverse('rentaltransaction-detail', args=[self.rental_transaction.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_rental_transaction(self):
        transaction_to_update = RentalTransaction.objects.first()
        url = reverse('rentaltransaction-detail', args=[transaction_to_update.pk])
        updated_data = {
            'uav': transaction_to_update.uav.pk,
            'user': transaction_to_update.user.pk,
            'start_date': transaction_to_update.start_date,
            'end_date': transaction_to_update.end_date + timedelta(hours=1),
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that the transaction was updated
        transaction_to_update.refresh_from_db()
        self.assertEqual(transaction_to_update.end_date, updated_data['end_date'])