from django.test import TestCase
from django.contrib.auth import get_user_model
from dronerental.rentalservice.models import UAV, RentalTransaction, Brand, Category
from datetime import timedelta
from django.utils import timezone

class RentalTransactionTests(TestCase):

    def setUp(self):
        # Test kullanıcısı ve UAV örneği oluştur
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        # brand
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

    def test_rental_transaction_creation(self):
        # Rental Transaction oluştur
        start_date = timezone.now()
        end_date = start_date + timedelta(hours=2)
        rental = RentalTransaction.objects.create(
            uav=self.uav,
            user=self.user,
            start_date=start_date,
            end_date=end_date,
        )

        # Doğrulamalar
        self.assertEqual(rental.uav, self.uav)
        self.assertEqual(rental.user, self.user)
        self.assertAlmostEqual(rental.total_cost, 200, places=2)


